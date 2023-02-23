from django.db import models

# Create your models here.
class Store(models.Model):
    store_id = models.CharField(max_length=100, primary_key=True)
    timezone_str = models.CharField(max_length=100, default='America/Chicago')

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"

    def __str__(self):
        return f"{self.store_id} - {self.timezone_str}"


class BusinessHour(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='business_hour'
    )
    day_of_week = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f"{self.store} - {self.day_of_week} - {self.start_time_local} to {self.end_time_local}"


class StoreStatus(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.store} - {self.timestamp_utc} - {self.status}"
