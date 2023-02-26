from django.core.management.base import BaseCommand, CommandError
from stores.models import BusinessHour, Store
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Caches business hours for all stores'

    def handle(self, *args, **options):
        try:
            # Cache business hours for all stores
            stores = Store.objects.all()
            for store in stores:
                store_cache_key = f"business_hours_{store.store_id}"
                cache.delete(store_cache_key)
                business_hours = BusinessHour.objects\
                    .filter(store__store_id=store.store_id)\
                    .values('day_of_week', 'start_time_local', 'end_time_local')

                if business_hours.exists():
                    cache.set(store_cache_key, list(business_hours), timeout=None)

        except Exception as e:
            print(f"Error: {e}")
