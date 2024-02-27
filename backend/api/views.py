import xlwt
from django.db.models import Count
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from ambassadors.models import Ambassadors, Content, ContentType, StudyProgramm
from api.filters import AmbassadorsFilter
from api.serializers import (AmbassadorPostSerializer, AmbassadorSerializer,
                             AmbassadorUpdateSerializer, BudgetSerializer,
                             ContentListSerializer, ContentPostSerializer,
                             ContentUpdateSerializer, StudyProgrammSerializer,
                             SupervisorSerializer)
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
        if self.action == 'update_content_status':
            return ContentUpdateSerializer
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
        print(budget)
        serializer = BudgetSerializer(budget, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['put', 'patch'], url_path='contentStatus')
    def update_content_status(self, request, pk=None):
        '''Обновление статуса контента для амбассадора.'''

        title = request.data.get('title')
        try:
            content_type = ContentType.objects.get(
                ambassador=self.get_object(),
                title=title
            )
            serializer = ContentUpdateSerializer(
                content_type, data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        except ContentType.DoesNotExist:
            return Response(
                {'error': 'Тип контента с указанным названием не найден, ' +
                 f'либо Пользователь еще не дошел до "{title}"'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

        rows = Budget.objects.all().values_list(
            'ambassador__name', 'merch__date', 'merch__merch__name',
            'merch__merch__cost'
        )
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response


class ContentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для Контента'''

    filter_backends = (DjangoFilterBackend,)
    filterset_class = AmbassadorsFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ContentListSerializer
        return ContentPostSerializer

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return Ambassadors.objects.annotate(
                content_count=Count('content_types__contents')
            ).filter(content_count__gt=0)
        return Content.objects.all()
