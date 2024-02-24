from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.permissions import SAFE_METHODS

from api.serializers import (AmbassadorPostSerializer, AmbassadorSerializer,
                             AmbassadorUpdateSerializer, SupervisorSerializer,
                             StudyProgrammSerializer)
from api.filters import AmbassadorsFilter
from ambassadors.models import Ambassadors, StudyProgramm
from users.models import CrmUser


class AmbassadorsViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для амбассадоров'''
    queryset = Ambassadors.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AmbassadorsFilter
    filterset_fields = ['study_programm', 'status', 'gender', 'country',
                        'city', 'want_to_do', 'date_from', 'date_to',
                        'supervisor']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AmbassadorSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return AmbassadorUpdateSerializer
        return AmbassadorPostSerializer


class StudyProgrammViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для программ обучения'''
    queryset = StudyProgramm.objects.all()
    serializer_class = StudyProgrammSerializer


class SupervisorViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для Кураторов'''
    queryset = CrmUser.objects.all()
    serializer_class = SupervisorSerializer
