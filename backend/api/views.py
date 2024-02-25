import io
import pandas as pd
from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import AmbassadorsSerializer, BudgetSerializer
from ambassadors.models import Ambassadors
from merch.models import Budget


class AmbassadorsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для магазинов'''
    queryset = Ambassadors.objects.all()
    serializer_class = AmbassadorsSerializer

    @action(detail=True, methods=['get'])
    def budget(self, request, pk=None):
        '''Средства на амбассадоре'''
        ambassador = self.get_object()
        budget = Budget.objects.filter(ambassador=ambassador)
        serializer = BudgetSerializer(budget)

        return Response(serializer.data)


class BudgetViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    @action(detail=True, methods=['get'])
    def report_budget(request):
        queryset = Budget.objects.all().order_by('ambassador')
        data = pd.DataFrame(list(queryset.values()))
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        data.to_excel(writer, sheet_name='Бюджет', index=False)

        writer.save()
        output.seek(0)

        response = HttpResponse(
            output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=budget.xlsx'
        return response
