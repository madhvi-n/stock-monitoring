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
    pass
