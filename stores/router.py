from rest_framework_nested import routers
from stores.views import (
    StoreViewSet, StoreReportViewSet,
    BusinessHourViewSet, StoreStatusViewSet
)

router = routers.SimpleRouter()
router.register(r'stores', StoreViewSet)
store_router = routers.NestedSimpleRouter(
    router, r'stores', lookup='store'
)
store_router.register(r'reports', StoreReportViewSet)
store_router.register(r'business_hours', BusinessHourViewSet)
store_router.register(r'updates', StoreStatusViewSet)
