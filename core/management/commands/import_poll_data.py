from django.core.management.base import BaseCommand, CommandError
from stores.models import BusinessHour, Store, StoreStatus
import csv
from django.conf import settings
from django.db import transaction, IntegrityError
from datetime import datetime
import pytz


class Command(BaseCommand):
    help = 'Loads poll data from CSV file into the database'

    def handle(self, *args, **options):
        try:
            csv_file = settings.STORE_STATUS_CSV_URL
            # Load Store data from CSV
            data = []
            with open(csv_file, 'r') as status_data:
                reader = csv.DictReader(status_data)
                for row in reader:
                    datetime_obj = datetime.strptime(row['timestamp_utc'][:-4], '%Y-%m-%d %H:%M:%S.%f')

                    # Convert the datetime object to UTC timezone
                    datetime_obj_utc = pytz.utc.localize(datetime_obj)

                    store, created = Store.objects.get_or_create(store_id=row['store_id'])
                    if created:
                        # This store does not have any business hours at this point
                        pass

                    # to avoid duplicates
                    if StoreStatus.objects.filter(
                        store=store,
                        status=row['status'],
                        timestamp_utc=datetime_obj_utc).exists():
                        pass
                    else:
                        store_status = StoreStatus(
                            store=store,
                            status=row['status'],
                            timestamp_utc=datetime_obj_utc
                        )
                        data.append(store_status)

                try:
                    with transaction.atomic():
                        StoreStatus.objects.bulk_create(data)
                except IntegrityError as e:
                    pass

        except FileNotFoundError:
            print(f"Error: file '{filename}' not found.")

        except ValueError as e:
            print(f"Error: CSV file '{filename}' contains invalid data. {str(e)}")
