from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django_filters.rest_framework import FilterSet, filters

from ambassadors.models import Ambassadors, StudyProgramm
from merch.models import Budget, Merch
from users.models import CrmUser


class AmbassadorsFilter(FilterSet):
    study_programm = filters.ModelMultipleChoiceFilter(
        queryset=StudyProgramm.objects.all()
    )
    supervisor = filters.ModelMultipleChoiceFilter(
        queryset=CrmUser.objects.all()
    )
    status = filters.MultipleChoiceFilter(choices=Ambassadors.STATUS)
    gender = filters.MultipleChoiceFilter(choices=Ambassadors.GENDER)
    country = filters.MultipleChoiceFilter(
        choices=Ambassadors.objects.values_list('country',
                                                'country').distinct()
    )
    city = filters.MultipleChoiceFilter(
        choices=Ambassadors.objects.values_list('city', 'city').distinct()
    )
    want_to_do = filters.MultipleChoiceFilter(
        choices=Ambassadors.objects.values_list('want_to_do',
                                                'want_to_do').distinct()
    )
    date_from = filters.DateFilter(field_name='date_created',
                                   lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date_created',
                                 lookup_expr='lte')

    class Meta:
        model = Ambassadors
        fields = ['study_programm', 'supervisor', 'status', 'gender',
                  'country', 'city', 'want_to_do', 'date_from', 'date_to']


class BudgetFilter(FilterSet):
    name = filters.CharFilter(method='filter_by_full_name')
    study_programm = filters.ModelMultipleChoiceFilter(
        field_name=('ambassador__study_programm'),
        queryset=StudyProgramm.objects.all()
    )
    status = filters.MultipleChoiceFilter(
        field_name=('ambassador__status'),
        choices=Ambassadors.STATUS
    )
    gender = filters.MultipleChoiceFilter(
        field_name=('ambassador__gender'),
        choices=Ambassadors.GENDER
    )
    city = filters.MultipleChoiceFilter(
        field_name=('ambassador__city'),
        choices=Ambassadors.objects.values_list('city', 'city').distinct()
    )
    date_from = filters.DateFilter(
        field_name='ambassador__date_created', lookup_expr='gte'
    )
    date_to = filters.DateFilter(
        field_name='ambassador__date_created', lookup_expr='lte'
    )
    date_shipping_from = filters.DateFilter(
        field_name='merch__date', lookup_expr='gte'
    )
    date_shipping_to = filters.DateFilter(
        field_name='merch__date', lookup_expr='lte'
    )
    merch = filters.CharFilter(
        field_name='merch__merch__name',
    )
    
    class Meta:
        model = Budget
        fields = ['study_programm', 'status', 'gender', 'name', 'date_shipping_from',
                  'date_shipping_to', 'city', 'date_from', 'date_to', 'merch']

    def filter_by_full_name(self, queryset, name, value):
        return queryset.annotate(
            ambassador_full_name=Concat('ambassador__surname', Value(' '), 'ambassador__name', Value(' '), 'ambassador__patronymic', output_field=CharField())
        ).filter(ambassador_full_name__icontains=value)
