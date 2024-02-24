from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import SAFE_METHODS

from ambassadors.models import Ambassadors, Content
from api.serializers import (AmbassadorsSerializer, ContentListSerializer,
                             ContentSerializer)


class AmbassadorsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для магазинов'''
    queryset = Ambassadors.objects.all()
    serializer_class = AmbassadorsSerializer


class ContentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для Контента'''

    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ContentListSerializer
        return ContentSerializer
