from rest_framework import filters

class AmbassadorFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Получите параметры фильтрации из запроса
        gender = request.query_params.get('gender', None)
        registration_date = request.query_params.get('registrationDate', None)
        program = request.query_params.get('program', None)
        status = request.query_params.get('status', None)
        city = request.query_params.get('city', None)

        # Примените фильтры, если параметры присутствуют
        if gender:
            queryset = queryset.filter(ambassador__gender=gender)
        if registration_date:
            queryset = queryset.filter(
                ambassador__registration_date=registration_date
            )
        if program:
            queryset = queryset.filter(ambassador__program=program)
        if status:
            queryset = queryset.filter(ambassador__status=status)
        if city:
            queryset = queryset.filter(ambassador__city=city)
        
        return queryset


class MerchFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Получите параметры фильтрации из запроса
        merch_style = request.query_params.get('merchStyle', None)
        shipped = request.query_params.get('shipped', None)
        shipped_from = request.query_params.get('shippedFrom', None)
        shipped_to = request.query_params.get('shippedTo', None)

        # Примените фильтры, если параметры присутствуют
        if merch_style:
            queryset = queryset.filter(merch__name=merch_style)
        if shipped:
            queryset = queryset.filter(shipped=shipped.lower() == 'true')
        if shipped_from:
            queryset = queryset.filter(date__gte=shipped_from)
        if shipped_to:
            queryset = queryset.filter(date__lte=shipped_to)

        return queryset