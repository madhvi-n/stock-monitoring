from django.contrib import admin
from stores.models import Store, BusinessHour, StoreStatus, StoreReport

# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_id', 'timezone_str',)
    search_fields = ('store_id',)

@admin.register(StoreStatus)
class StoreStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'status', 'timestamp_utc')
    list_filter = ('store', 'status',)
    search_fields = ('store',)


@admin.register(BusinessHour)
class BusinessHourAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'store', 'day_of_week', 'start_time_local', 'end_time_local'
    )
    list_filter = ('store', )
    search_fields = ('store',)


@admin.register(StoreReport)
class StoreReportAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'store', 'uptime_last_day', 'uptime_last_hour', 'uptime_last_week',
        'downtime_last_day', 'downtime_last_hour', 'downtime_last_week',
    )
    search_fields = ('store',)
