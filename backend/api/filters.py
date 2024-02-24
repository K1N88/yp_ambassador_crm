from django_filters.rest_framework import FilterSet, filters

from ambassadors.models import Ambassadors, StudyProgramm
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
