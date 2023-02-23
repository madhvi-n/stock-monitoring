import csv
import requests
from io import StringIO
from django.utils import timezone
from celery import shared_task
from .models import Store, BusinessHour
from django.db import transaction
import datetime

@shared_task
def update_stores_from_csv():
    # Download and parse the store data CSV
    stores_data = requests.get("https://drive.google.com/uc?id=1UIx1hVJ7qt_6oQoGZgb8B3P2vd1FD025").text
    stores_reader = csv.DictReader(StringIO(stores_data))

    # Download and parse the business hours CSV
    business_hours_data = requests.get("https://drive.google.com/uc?id=1va1X3ydSh-0Rt1hsy2QSnHRA4w57PcXg").text
    business_hours_reader = csv.DictReader(StringIO(business_hours_data))

    # # Download and parse the timezone data CSV
    timezone_data = requests.get("https://drive.google.com/uc?id=101P9quxHoMZMZCVWQ5o-shonk2lgK1-o").text
    timezone_reader = csv.DictReader(StringIO(timezone_data))

    # Create a lookup table for timezones
    timezone_lookup = {row['store_id']: row['timezone_str'] for row in timezone_reader}

    with transaction.atomic():
    #     # Process each row in the stores data CSV
        for row in stores_reader:
            store_id = row['store_id']
            status = row['status']
            timestamp = timezone.make_aware(datetime.datetime.strptime(row['timestamp_utc'], '%Y-%m-%d %H:%M:%S'))

            # Get the timezone for this store
            timezone_str = timezone_lookup.get(store_id, 'America/Chicago')

            # Look up or create the store
            store, _ = Store.objects.get_or_create(store_id=store_id, timezone_str=timezone_str)

            # Create a new store status object and save it
            StoreStatus.objects.create(store=store, timestamp=timestamp, status=status)

        # Process each row in the business hours CSV
        # for row in business_hours_reader:
        #     store_id = row['store_id']
        #     day_of_week = int(row['day'])
        #     start_time = datetime.datetime.strptime(row['start_time_local'], '%Y-%m-%d %H:%M:%S').time()
        #     end_time = datetime.datetime.strptime(row['end_time_local'], '%Y-%m-%d %H:%M:%S').time()
        #
        #     # Look up or create the store
        #     store, _ = Store.objects.get_or_create(store_id=store_id)
        #
        #     # Create a new business hour object and save it
        #     business_hour = BusinessHour(store=store, day_of_week=day_of_week, start_time=start_time, end_time=end_time)
        #     business_hour.save()
        #
