from django.urls import path, include
from .router import router, store_router

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(store_router.urls)),
]
