from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .mixins import (
    PaginatedResponseMixin,
    MultiSerializerViewSetMixin,
    DestroyModelMixin,
)

class BaseReadOnlyViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        MultiSerializerViewSetMixin,
        PaginatedResponseMixin,
        viewsets.GenericViewSet):
    pass


class BaseViewSet(
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        DestroyModelMixin,
        BaseReadOnlyViewSet):
    pass
