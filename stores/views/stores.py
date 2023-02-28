from core.views import BaseReadOnlyViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from stores.models import Store
from stores.serializers import StoreSerializer, StoreDetailSerializer
from stores.services import generate_store_report


class StorePagination(PageNumberPagination):
    page_size = 50


class StoreViewSet(BaseReadOnlyViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer
    pagination_class = StorePagination
    lookup_field = 'store_id'
    serializer_action_classes = {
        'list': StoreSerializer
    }

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginated_response(queryset)

    def retrieve(self, request, store_id=None):
        store = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(store)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, store_id=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, store_id=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True)
    def trigger_report(self, request, store_id=None):
        store = self.get_object()
        report = generate_store_report(store.store_id)
        return Response({"report_id": report.id}, status=status.HTTP_200_OK)
