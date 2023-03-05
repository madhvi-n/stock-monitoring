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
            with open(csv_file, 'r') as status_data:
                reader = csv.DictReader(status_data)
                data = []
                for row in reader:
                    datetime_obj = datetime.strptime(row['timestamp_utc'][:-4], '%Y-%m-%d %H:%M:%S.%f')
                    datetime_obj_utc = pytz.utc.localize(datetime_obj)
                    store = Store.objects.filter(store_id=row['store_id']).last()
                    if store is not None:
                        store_status = StoreStatus(
                            store=store,
                            status=row['status'],
                            timestamp_utc=datetime_obj_utc
                        )
                        data.append(store_status)
                try:
                    with transaction.atomic():
                        created_objects = StoreStatus.objects.bulk_create(data)
                        print(f'Poll data inserted in database successfully at {datetime.now()}. \n {len(created_objects)} objects were created successfully.')
                except IntegrityError as e:
                    pass

        except FileNotFoundError:
            print(f"Error: file '{csv_file}' not found.")

        except ValueError as e:
            print(f"Error: CSV file '{csv_file}' contains invalid data. {str(e)}")
