from core.views import BaseReadOnlyViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from stores.models import StoreReport
from stores.serializers import StoreReportSerializer, StoreReportDetailSerializer


class StoreReportPagination(PageNumberPagination):
    page_size = 50


class StoreReportViewSet(BaseReadOnlyViewSet):
    queryset = StoreReport.objects.all()
    serializer_class = StoreReportDetailSerializer
    pagination_class = StoreReportPagination

    serializer_action_classes = {
        'list': StoreReportSerializer
    }

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs != {}:
            if 'store_id' in self.kwargs:
                return self.queryset.filter(store__store_id=self.kwargs['store_id'])
        return queryset

    def list(self, request, store_store_id=None):
        # return last report object id
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, store_store_id=None, pk=None):
        report = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, store_store_id=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, store_store_id=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)
