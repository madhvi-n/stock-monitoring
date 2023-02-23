from django.contrib import admin
from stores.models import Store, BusinessHour, StoreStatus

# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_id', 'timezone_str',)


@admin.register(StoreStatus)
class StoreStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'status',)


@admin.register(BusinessHour)
class BusinessHourAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'day_of_week',)
