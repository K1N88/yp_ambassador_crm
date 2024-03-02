from django_filters import (FilterSet, CharFilter, DateFilter,
                            BooleanFilter, MultipleChoiceFilter,
                            ModelMultipleChoiceFilter)

from .models import MerchForSend
from ambassadors.models import Ambassadors, StudyProgramm

class MerchFilter(FilterSet):
    
    gender = MultipleChoiceFilter(choices=Ambassadors.GENDER)
    registrationDate = DateFilter(field_name='ambassador__registration_date', lookup_expr='exact')
    program = ModelMultipleChoiceFilter(
        queryset=StudyProgramm.objects.all()
    )
    status = MultipleChoiceFilter(choices=Ambassadors.STATUS)
    city = CharFilter(field_name='ambassador__city', lookup_expr='exact')
    merchStyle = CharFilter(field_name='merch__name', lookup_expr='exact')
    shipped = BooleanFilter(field_name='shipped')
    date = DateFilter(field_name='date', lookup_expr='exact')
    shippedFrom = DateFilter(field_name='date', lookup_expr='gte')
    shippedTo = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = MerchForSend
        fields = '__all__'