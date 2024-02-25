# from rest_framework import filters

# class AmbassadorFilterBackend(filters.BaseFilterBackend):
    
#     def filter_queryset(self, request, queryset, view):
#         """
#         Filter queryset based on ambassador attributes.

#         Parameters:
#         - `gender`: Gender of the ambassador.
#         - `registrationDate`: Registration date of the ambassador.
#         - `program`: Ambassador's program.
#         - `status`: Ambassador's status.
#         - `city`: Ambassador's city.

#         Example:
#         GET /api/merchandise/?gender=male&registrationDate=2022-01-01&program=some_program&status=some_status&city=some_city
#         """
#         # Получите параметры фильтрации из запроса
#         gender = request.query_params.get('gender', None)
#         registration_date = request.query_params.get('registrationDate', None)
#         program = request.query_params.get('program', None)
#         status = request.query_params.get('status', None)
#         city = request.query_params.get('city', None)

#         # Примените фильтры, если параметры присутствуют
#         if gender:
#             queryset = queryset.filter(ambassador__gender=gender)
#         if registration_date:
#             queryset = queryset.filter(
#                 ambassador__registration_date=registration_date
#             )
#         if program:
#             queryset = queryset.filter(ambassador__program=program)
#         if status:
#             queryset = queryset.filter(ambassador__status=status)
#         if city:
#             queryset = queryset.filter(ambassador__city=city)
        
#         return queryset


# class MerchFilterBackend(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         # Получите параметры фильтрации из запроса
#         merch_style = request.query_params.get('merchStyle', None)
#         shipped = request.query_params.get('shipped', None)
#         shipped_from = request.query_params.get('shippedFrom', None)
#         shipped_to = request.query_params.get('shippedTo', None)

#         # Примените фильтры, если параметры присутствуют
#         if merch_style:
#             queryset = queryset.filter(merch__name=merch_style)
#         if shipped:
#             queryset = queryset.filter(shipped=shipped.lower() == 'true')
#         if shipped_from:
#             queryset = queryset.filter(date__gte=shipped_from)
#         if shipped_to:
#             queryset = queryset.filter(date__lte=shipped_to)

#         return queryset

from django_filters import FilterSet, CharFilter, DateFilter, BooleanFilter, MultipleChoiceFilter, ModelMultipleChoiceFilter
from django.db.models import Q

from .models import MerchForSend
from ambassadors.models import Ambassadors, StudyProgramm

class MerchFilter(FilterSet):
    
    gender = MultipleChoiceFilter(choices=Ambassadors.GENDER)
    # gender = CharFilter(field_name='ambassador__gender', lookup_expr='exact')
    registrationDate = DateFilter(field_name='ambassador__registration_date', lookup_expr='exact')
    # program = CharFilter(field_name='ambassador__program', lookup_expr='exact')
    program = ModelMultipleChoiceFilter(
        queryset=StudyProgramm.objects.all()
    )
    status = MultipleChoiceFilter(choices=Ambassadors.STATUS)
    # status = CharFilter(field_name='ambassador__status', lookup_expr='exact')
    city = CharFilter(field_name='ambassador__city', lookup_expr='exact')
    merchStyle = CharFilter(field_name='merch__name', lookup_expr='exact')
    shipped = BooleanFilter(field_name='shipped')
    date = DateFilter(field_name='date', lookup_expr='exact')
    shippedFrom = DateFilter(field_name='date', lookup_expr='gte')
    shippedTo = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = MerchForSend
        fields = '__all__'