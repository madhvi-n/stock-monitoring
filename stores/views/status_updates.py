from core.views import BaseReadOnlyViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from stores.models import StoreStatus
from stores.serializers import StoreStatusSerializer


class StoreStatusPagination(PageNumberPagination):
    page_size = 50


class StoreStatusViewSet(BaseReadOnlyViewSet):
    queryset = StoreStatus.objects.all()
    serializer_class = StoreStatusSerializer
    pagination_class = StoreStatusPagination

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs != {}:
            if 'store_store_id' in self.kwargs:
                return self.queryset.filter(store__store_id=self.kwargs['store_store_id'])
        return queryset

    # def list(self, request, store_store_id=None):
    #     return Response(status=status.HTTP_403_FORBIDDEN)

    # def retrieve(self, request, store_store_id=None, pk=None):
    #     return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, store_store_id=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, store_store_id=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)
