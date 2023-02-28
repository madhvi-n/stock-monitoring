from core.views import BaseReadOnlyViewSet
from stores.models import BusinessHour
from stores.serializers import BusinessHourSerializer

class BusinessHourViewSet(BaseReadOnlyViewSet):
    queryset = BusinessHour.objects.all().order_by('day_of_week')
    serializer_class = BusinessHourSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs != {}:
            if 'store_store_id' in self.kwargs:
                return self.queryset.filter(store__store_id=self.kwargs['store_store_id'])
        return queryset

    # def list(self, request, store_store_id=None):
    #     return Response(status=status.HTTP_403_FORBIDDEN)
    
    def retrieve(self, request, store_store_id=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, store_store_id=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, store_store_id=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)
