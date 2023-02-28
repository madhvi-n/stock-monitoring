from rest_framework import serializers
from stores.models import Store, BusinessHour, StoreStatus, StoreReport
import serpy
import pytz


class StoreSerializer(serpy.Serializer):
    store_id = serpy.StrField()
    timezone_str = serpy.StrField()


class StoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('store_id', 'timezone_str')


class StoreStatusSerializer(serpy.Serializer):
    store = StoreSerializer()
    timestamp_utc = serpy.Field()
    status = serpy.StrField()
    timestamp_tz = serpy.MethodField()

    # For testing
    def get_timestamp_tz(self, obj):
        if hasattr(obj, 'timestamp_utc'):
            store_tz = pytz.timezone(obj.store.timezone_str)
            return obj.timestamp_utc.astimezone(store_tz)
        return None


class StoreStatusDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreStatus
        fields = ('store',  'timestamp_utc', 'status')


class BusinessHourSerializer(serpy.Serializer):
    store = StoreSerializer()
    day_of_week = serpy.IntField()
    start_time_local = serpy.Field()
    start_time_local = serpy.Field()


class BusinessHourDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHour
        fields = (
            'store',  'day_of_week', 'start_time_local', 'end_time_local'
        )


class StoreReportSerializer(serpy.Serializer):
    store = StoreSerializer()
    uptime_last_hour = serpy.FloatField()
    uptime_last_day = serpy.FloatField()
    uptime_last_week = serpy.FloatField()
    downtime_last_hour = serpy.FloatField()
    downtime_last_day = serpy.FloatField()
    downtime_last_week = serpy.FloatField()


class StoreReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReport
        fields = (
            'store', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week',
            'downtime_last_hour', 'downtime_last_day', 'downtime_last_week'
        )
