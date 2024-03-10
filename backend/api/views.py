import xlwt
import logging
import pandas as pd
from xlwt import easyxf

from django.db.models import Count, Max, Sum
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action, api_view
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response

from ambassadors.models import Ambassadors, Content, ContentType, StudyProgramm
from api.filters import AmbassadorsFilter, BudgetFilter
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
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для амбассадоров'''
    queryset = Ambassadors.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AmbassadorsFilter
    filterset_fields = ['study_programm', 'status', 'gender', 'country',
                        'city', 'want_to_do', 'date_from', 'date_to',
                        'supervisor']

    def get_permissions(self):
        if self.action == 'create':
            return (AllowAny(),)
        return (IsAuthenticated(),)

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
        serializer = BudgetSerializer(budget, many=True)

        return Response(serializer.data)

    @action(
        detail=True,
        methods=['put', 'patch'],
        url_path='contentStatus'
    )
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

    @action(
        detail=True,
        methods=['delete'],
        url_path=r'content/(?P<content_id>\d+)'
    )
    def delete_content(self, request, pk=None, content_id=None):
        '''Удаление контента для амбассадора.'''

        ambassador = self.get_object()
        try:
            Content.objects.get(
                id=content_id,
                content_type__ambassador=ambassador
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Content.DoesNotExist:
            return Response(
                {'error': 'Контент с указанным ID не найден, ' +
                 'Проверьте корректность ввода ContentId'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
    filterset_class = BudgetFilter
    filterset_fields = ['study_programm', 'status', 'gender', 'name', 'date_shipping_from',
                        'date_shipping_to', 'city', 'date_from', 'date_to', 'merch']

    def get_queryset(self):
        queryset = Budget.objects.all()

        filterset = self.filterset_class(data=self.request.GET, queryset=queryset)
        queryset = filterset.qs

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_spending = queryset.aggregate(total_spending=Sum('merch__merch__cost'))

        serializer = self.get_serializer(queryset, many=True)
        response_data = {"total_spending": total_spending['total_spending'], "results": serializer.data}
        
        return Response(response_data)

    @action(detail=False, methods=['get'])
    def excel(self, request):
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="budget.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Budget')

            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Имя', 'Дата отправки', 'Тип мерча', 'Стоимость']

            borders = xlwt.Borders()
            borders.left = xlwt.Borders.THIN
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN

            align_center = xlwt.Alignment()
            align_center.horz = xlwt.Alignment.HORZ_CENTER

            style_center = xlwt.XFStyle()
            style_center.alignment = align_center
            style_center.borders = borders

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], style_center)

            font_style = xlwt.XFStyle()

            date_style = easyxf('font: bold off; pattern: pattern solid, fore_colour white; '
                                'borders: left thin, right thin, top thin, bottom thin;')
            date_style.num_format_str = 'DD.MM.YYYY'

            total_cost = 0

            rows = Budget.objects.all().values_list(
                'ambassador__name', 'merch__date', 'merch__merch__name', 'merch__merch__cost'
            )
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    if col_num == 1:
                        ws.write(row_num, col_num, row[col_num], date_style)
                    else:
                        ws.write(row_num, col_num, row[col_num], style_center)
                total_cost += row[3]

            ws.write(row_num+1, 3, 'Итог:', font_style)
            ws.write(row_num+1, 4, total_cost, font_style)

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
                latest_content_date=Max('content_types__contents__created_at'),
                content_count=Count('content_types__contents')
            ).filter(content_count__gt=0).order_by('-latest_content_date')
        return Content.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return (AllowAny(),)
        return (IsAuthenticated(),)


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
