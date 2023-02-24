from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status


class PaginatedResponseMixin(object):
    def paginated_response(self, queryset, context=None, paginator=None, fields=None):
        """
        This function should be called when a paginated response is needed
        """
        page = None

        if paginator is not None:
            page = paginator.paginate_queryset(queryset, request=self.request)
        else:
            page = self.paginate_queryset(queryset)

        if page is not None:
            kwargs = {}
            if fields is not None:
                kwargs = {'fields': fields}
            serializer = self.get_serializer(page, context=context, many=True, **kwargs)
            if paginator is not None:
                return paginator.get_paginated_response(serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, context=context, many=True, fields=fields)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': True }, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
