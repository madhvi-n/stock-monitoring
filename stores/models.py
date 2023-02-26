from django.db import models
from django.utils import timezone
import pytz
from datetime import datetime
from django.db.models import ExpressionWrapper, F, Func, Value


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Store(TimeStampedModel):
    store_id = models.CharField(max_length=255, unique=True)
    timezone_str = models.CharField(max_length=255, default='America/Chicago')

    def __str__(self):
        return f"{self.store_id}"


class BusinessHour(TimeStampedModel):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='business_hours'
    )
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    class Meta:
        unique_together = ('store', 'day_of_week')
        verbose_name = "Business Hour"
        verbose_name_plural = "Business Hours"


    def __str__(self):
        return f'{self.store}: {self.get_day_of_week_display()} {self.start_time_local} - {self.end_time_local}'


class StoreStatus(TimeStampedModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='status_updates'
    )
    timestamp_utc = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    @classmethod
    def convert_from_utc(cls, timestamp_utc):
        tz = pytz.timezone(cls.store.timezone_str)
        local_timestamp = timestamp_utc.astimezone(tz)
        return local_timestamp


    class Meta:
        unique_together = ('store', 'timestamp_utc')
        verbose_name = "Store Status"
        verbose_name_plural = "Store Statuses"

    def __str__(self):
        return f'{self.store}: {self.timestamp_utc} {self.status}'


class StoreReport(TimeStampedModel):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="reports"
    )
    uptime_last_hour = models.PositiveIntegerField(default=0)
    uptime_last_day = models.PositiveIntegerField(default=0)
    uptime_last_week = models.PositiveIntegerField(default=0)
    downtime_last_hour = models.PositiveIntegerField(default=0)
    downtime_last_day = models.PositiveIntegerField(default=0)
    downtime_last_week = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Store Report"
        verbose_name_plural = "Store Reports"

    def __str__(self):
        return f"""{self.store}:
            Uptime - {self.uptime_last_day} last day,
            {self.uptime_last_week} last week.
            Downtime - {self.downtime_last_day} last day, {self.downtime_last_week} last week."""
