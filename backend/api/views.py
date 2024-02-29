import xlwt

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS

from api.serializers import (AmbassadorPostSerializer, AmbassadorSerializer,
                             AmbassadorUpdateSerializer, SupervisorSerializer,
                             StudyProgrammSerializer, BudgetSerializer)
from api.filters import AmbassadorsFilter
from ambassadors.models import Ambassadors, StudyProgramm
from merch.models import Budget
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

    @action(detail=True, methods=['get'])
    def budget(self, request, pk=None):
        '''Средства на амбассадора'''
        ambassador = self.get_object()
        budget = Budget.objects.filter(ambassador=ambassador)
        serializer = BudgetSerializer(budget, many=True)

        return Response(serializer.data)


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


class BudgetViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    @action(detail=False, methods=['get'])
    def excel(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="budget.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Budget')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Имя', 'Дата отправки', 'Тип мерча', 'Стоимость', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = Budget.objects.all().values_list('ambassador__name', 'merch__date',
                                                'merch__merch__name', 'merch__merch__cost')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
