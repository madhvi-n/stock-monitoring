from stores.models import BusinessHour, Store, StoreReport, StoreStatus
from django.core.cache import cache
from datetime import datetime, timedelta
import pytz
from django.db.models.functions import ExtractWeekDay, TruncDate, Cast, Concat, Extract
from django.db.models import Count, F, Q, Value, CharField, Sum, ExpressionWrapper
from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.utils.timezone import timezone, datetime, timedelta


def calculate_uptime(statuses, start_time, end_time):
    """Returns uptime (in seconds) for given statuses and time intervals"""
    try:
        prev_timestamp = start_time
        prev_status = None
        uptime = 0

        for timestamp, status in statuses:
            if prev_status is None:
                if status == 'active':
                    # If the first status is active, consider the time from start_time to this timestamp as active time
                    uptime += (timestamp - start_time).total_seconds()
                # If the first status is inactive, do nothing since we haven't accumulated any active time yet
            else:
                if status == 'active':
                    # If the current status is active, add the time difference between the previous and current timestamp
                    uptime += (timestamp - prev_timestamp).total_seconds()
                else:
                    # If the current status is inactive, it's downtime
                    continue
            prev_status = status
            prev_timestamp = timestamp

        if prev_status == 'active' and prev_timestamp < end_time:
            uptime += (end_time - prev_timestamp).total_seconds()
        return uptime
    except Exception as e:
        print(f"Error in function: {e}")


def generate_store_report(store_id: str):
    """ Generates Store Report"""
    try:
        store = Store.objects.get(store_id=store_id)

        if store is None or not store.status_updates.exists():
            return

        store_tz = pytz.timezone(store.timezone_str)
        now_utc = datetime.now(pytz.utc)
        last_hour_utc = now_utc - timedelta(hours=1)
        last_day_utc = now_utc - timedelta(days=1)
        last_week_utc = now_utc - timedelta(days=7)

        try:
            start_time_local = datetime.min.time()
            end_time_local = datetime.max.time()

            business_hours = store.get_business_hours_by_day()

            business_hours_last_hour = business_hours[last_hour_utc.weekday()]
            start_time_last_hour_utc, end_time_last_hour_utc = [datetime.combine(last_hour_utc.date(), t, tzinfo=pytz.utc) for t in business_hours_last_hour]
            start_time_last_hour_local = start_time_last_hour_utc.astimezone(store_tz)
            end_time_last_hour_local = end_time_last_hour_utc.astimezone(store_tz)

            business_hour_last_day = business_hours[last_day_utc.weekday()]
            start_time_last_day_utc, end_time_last_day_utc = [datetime.combine(last_day_utc.date(), t, tzinfo=pytz.utc) for t in business_hour_last_day]
            start_time_last_day_local = start_time_last_day_utc.astimezone(store_tz)
            end_time_last_day_local = end_time_last_day_utc.astimezone(store_tz)

            # Query the store status table to get the status updates for the
            # past hour, day and week strictly during business hours

            # Calculate uptime last hour in minutes
            uptime_last_hour = 0
            downtime_last_hour = 0
            last_hour_statuses = store.status_updates.filter(
                Q(timestamp_utc__range=(last_hour_utc, now_utc)) &
                Q(timestamp_utc__range=(start_time_last_hour_utc, end_time_last_hour_utc))
            ).values_list('timestamp_utc', 'status').order_by('timestamp_utc')

            if last_hour_statuses.exists():
                uptime_last_hour = calculate_uptime(last_hour_statuses, start_time_last_hour_utc, end_time_last_hour_utc)
                uptime_last_hour /= 60
                downtime_last_hour = 60 - uptime_last_hour

            print(f"Uptime last hour: {uptime_last_hour} mins")
            print(f"Downtime last hour: {downtime_last_hour} mins")

            # Calculate uptime last day in hours
            uptime_last_day = 0
            downtime_last_day = 0
            last_day_statuses = store.status_updates.filter(
                Q(timestamp_utc__range=(last_day_utc, now_utc)) &
                Q(timestamp_utc__range=(start_time_last_day_utc, end_time_last_day_utc))
            ).values_list('timestamp_utc', 'status').order_by('timestamp_utc')

            if last_day_statuses.exists():
                uptime_last_day = calculate_uptime(last_day_statuses, start_time_last_day_utc, end_time_last_day_utc)
                uptime_last_day /= 3600
                total_hours = (end_time_last_day_utc - start_time_last_day_utc).total_seconds() / 3600
                downtime_last_day = total_hours - uptime_last_day

            print(f"Uptime last day: {uptime_last_day} hrs")
            print(f"Downtime last day: {downtime_last_day} hrs")

            # Calculate uptime last week in days
            # last_week_statuses = store.status_updates.filter(
            #     Q(timestamp_utc__range=(last_week_utc, now_utc)) &
            #     Q(timestamp_utc__range=(start_time_last_day_utc, end_time_last_day_utc))
            # ).values_list('timestamp_utc', 'status').order_by('timestamp_utc')
            # print(last_week_statuses, "last_week_statuses")


            # business_weekly_hours_in_seconds = 0
            # total_days = len(business_hours.keys())
            # for day_of_week, (interval_start, interval_end)  in business_hours.items():
            #     time_difference = (interval_end - interval_start).total_seconds()
            #     business_weekly_hours_in_seconds += time_difference
            #
            uptime_last_week = 0
            downtime_last_week = 0
            # weekly_uptime_in_seconds = 0

            # for weekly_start_time, weekly_end_time in business_hours.values():
                # fetch statuses by day and weekly_start_time and weekly_end_time
                # weekly_uptime_in_seconds += calculate_uptime per day
                # downtime = business_weekly_hours_in_seconds - uptime

                # if weekly_uptime_in_seconds:
                    # find downtime from total uptime convert uptime in days
            #         uptime_last_week = weekly_uptime_in_seconds / 86400
            #         downtime_last_week = (business_weekly_hours_in_seconds - weekly_uptime_in_seconds) / 86400
            # print(f"Uptime last week: {uptime_last_week} days")
            # print(f"Downtime last week: {uptime_last_week} days")

            report = StoreReport.objects.create(
                store=store,
                uptime_last_hour=uptime_last_hour,
                uptime_last_day=uptime_last_day,
                uptime_last_week=uptime_last_week,
                downtime_last_hour=downtime_last_hour,
                downtime_last_day=downtime_last_day,
                downtime_last_week=downtime_last_week
            )
            return report
        except Exception as e:
            return Exception(f"Error while calculating uptime and downtime: {e}")
    except Exception as e:
        print(f"Error: {e}")
        pass
