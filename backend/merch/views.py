import xlwt
from xlwt import easyxf

from django.http import HttpResponse
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import MerchForSend
from .serializers import MerchSerializer
from .filters import MerchFilter 


class MerchandiseView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = MerchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MerchFilter 

    def get_queryset(self):
        return MerchForSend.objects.all()

    @action(detail=False, methods=['get'])
    def excel(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="merch.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Merch')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        borders = xlwt.Borders()
        borders.bottom = xlwt.Borders.THIN
        font_style.borders = borders

        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        font_style.alignment = alignment

        columns = ['Имя', 'Тип мерча', 'Комментарий', 'Дата отправки', 'Статус']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = MerchForSend.objects.all().values_list(
            'ambassador__name', 'merch__name', 'comment', 'date', 'shipped'
        )
        date_style = easyxf('font: bold off; pattern: pattern solid, fore_colour white; '
                            'borders: left thin, right thin, top thin, bottom thin;')
        date_style.num_format_str = 'DD.MM.YYYY'

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                cell_style = xlwt.XFStyle()
                cell_style.borders = borders
                cell_style.alignment = alignment

                if col_num == 3:
                    ws.write(row_num, col_num, row[col_num], date_style)
                elif col_num == 4:
                    status = 'Отправлен' if row[col_num] else 'Не отправлен'
                    ws.write(row_num, col_num, status, cell_style)
                else:
                    ws.write(row_num, col_num, row[col_num], cell_style)

        wb.save(response)
        return response


class SetStatusView(APIView):
    def put(self, request, ambassadorId, merchandiseId):
        instance = MerchForSend.objects.get(pk=merchandiseId)
        serializer = MerchSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
