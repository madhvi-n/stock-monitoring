from io import StringIO
from datetime import datetime
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.db.models import Q, F

from stores.models import Store, BusinessHour, StoreStatus
from stores.services import generate_store_report

from celery import chain
import csv
import pytz


@shared_task
def insert_poll_data_in_database():
    """Inserts poll data from CSV in database"""

    csv_file = settings.STORE_STATUS_CSV_URL
    # Load Store data from CSV
    data = []
    with open(csv_file, 'r') as status_data:
        reader = csv.DictReader(status_data)
        for row in reader:
            # get the store object
            try:
                store = Store.objects.get(id=row['store_id'])
            except Store.DoesNotExist:
                continue  # skip to the next row if store doesn't exist

            # Convert timestamp into UTC object
            datetime_obj = datetime.strptime(row['timestamp_utc'][:-4], '%Y-%m-%d %H:%M:%S.%f')
            datetime_obj_utc = pytz.utc.localize(datetime_obj)

            # get the store status (active or inactive)
            status = row['status']

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
        print(f'Poll data inserted in database successfully at {datetime.now()}')


@shared_task
def create_status_reports():
    """ Generates Store Status Reports """
    stores = Store.objects.all()
    for store in stores:
        generate_store_report(store.store_id)


# Chain the tasks and run
task_chain = chain(insert_poll_data_in_database.si(), create_status_reports.si())
task_chain()
