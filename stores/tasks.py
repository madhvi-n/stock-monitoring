from io import StringIO
from datetime import datetime
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.db.models import Q, F
from django.db import transaction, IntegrityError
from stores.models import Store, BusinessHour, StoreStatus
from stores.services import generate_store_report

from celery import chain, shared_task
import csv
import pytz


@shared_task
def insert_poll_data_in_database():
    """Inserts poll data from CSV in database"""

    try:
        csv_file = settings.STORE_STATUS_CSV_URL

        # Load Store data from CSV
        with open(csv_file, 'r') as status_data:
            reader = csv.DictReader(status_data)
            data = []
            for row in reader:
                datetime_obj = datetime.strptime(row['timestamp_utc'][:-4], '%Y-%m-%d %H:%M:%S.%f')
                datetime_obj_utc = pytz.utc.localize(datetime_obj)
                store = Store.objects.get(store_id=row['store_id'])
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




# @shared_task
# def create_status_reports():
#     """ Generates Store Status Reports """
#     stores = Store.objects.all()
#     for store in stores:
#         generate_store_report(store.store_id)


# Chain the tasks and run
# task_chain = chain(insert_poll_data_in_database.si(), create_status_reports.si())
# task_chain()
