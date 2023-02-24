from django.core.management.base import BaseCommand, CommandError
from stores.models import Store
import csv
from django.conf import settings
from django.db import transaction, IntegrityError


class Command(BaseCommand):
    help = 'Loads store timezone data from CSV file into the database'

    def handle(self, *args, **options):
        try:
            csv_file = settings.STORE_TIMEZONES_CSV_URL
            # Load Store data from CSV
            data = []
            with open(csv_file, 'r') as store_timezones:
                reader = csv.DictReader(store_timezones)
                for row in reader:
                    store = Store(
                        store_id=row['store_id'],
                        timezone_str=row['timezone_str']
                    )
                    data.append(store)

                try:
                    with transaction.atomic():
                        Store.objects.bulk_create(data)
                except IntegrityError as e:
                    pass

        except FileNotFoundError:
            print(f"Error: file '{filename}' not found.")

        except ValueError as e:
            print(f"Error: CSV file '{filename}' contains invalid data. {str(e)}")
