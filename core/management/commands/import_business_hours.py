from django.core.management.base import BaseCommand, CommandError
from stores.models import BusinessHour, Store
from django.conf import settings
from django.db import transaction, IntegrityError
from django.core.cache import cache
from datetime import datetime
import csv
import json


class Command(BaseCommand):
    help = 'Loads business hours data from CSV file into the database'

    def handle(self, *args, **options):
        try:
            csv_file = settings.BUSINESS_HOURS_CSV_URL
            
            # Load Store data from CSV
            data = []
            with open(csv_file, 'r') as hours_data:
                reader = csv.DictReader(hours_data)
                for row in reader:
                    store, created = Store.objects.get_or_create(
                        store_id=row['store_id']
                    )
                    business_hour = BusinessHour(
                        store=store,
                        day_of_week=row['day'],
                        start_time_local=row['start_time_local'],
                        end_time_local=row['end_time_local']
                    )
                    data.append(business_hour)
                try:
                    with transaction.atomic():
                        BusinessHour.objects.bulk_create(data, ignore_conflicts=True)
                except IntegrityError as e:
                    # Handle the integrity error if needed
                    pass

        except FileNotFoundError:
            print(f"Error: file '{filename}' not found.")

        except ValueError as e:
            print(f"Error: CSV file '{filename}' contains invalid data. {str(e)}")
