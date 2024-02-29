import xlwt
import logging
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from ambassadors.models import Ambassadors, Content, StudyProgramm
from api.filters import AmbassadorsFilter
from api.serializers import (AmbassadorPostSerializer, AmbassadorSerializer,
                             AmbassadorUpdateSerializer, BudgetSerializer,
                             ContentListSerializer, ContentPostSerializer,
                             ContentUpdateSerializer, StudyProgrammSerializer,
                             SupervisorSerializer)
from merch.models import Budget
from users.models import CrmUser


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logger()


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
        print(budget)
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
        elif self.request.method in ['PUT', 'PATCH']:
            return ContentUpdateSerializer  # Доб. update в сер. ниже?
        return ContentPostSerializer

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return Ambassadors.objects.all()
        return Content.objects.all()


@api_view(['POST'])
def import_ambassadors(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    file = request.FILES['file']
    if not file.name.endswith('.xls') and not file.name.endswith('.xlsx'):
        return JsonResponse({'error': 'File must be in Excel format'},
                            status=400)

    try:
        df = pd.read_excel(file)
        ambassadors_data = df.to_dict(orient='records')
        ambassadors = []
        study_programm = StudyProgramm.objects.all()
        for item in ambassadors_data:
            item['study_programm'] = study_programm.get(
                pk=item['study_programm']
            )
            ambassadors.append(
                Ambassadors(**item)
            )
        Ambassadors.objects.bulk_create(ambassadors)

        return JsonResponse({'message': 'Ambassadors imported successfully'},
                            status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
