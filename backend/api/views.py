from rest_framework import viewsets, mixins

from api.serializers import AmbassadorsSerializer
from ambassadors.models import Ambassadors


class AmbassadorsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для магазинов'''
    queryset = Ambassadors.objects.all()
    serializer_class = AmbassadorsSerializer
