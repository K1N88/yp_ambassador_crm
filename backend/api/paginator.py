from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Кастомная пагинация."""
    
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_page_size(self, request):
        if 'page_size' in request.query_params:
            try:
                page_size = int(request.query_params['page_size'])
                if page_size > 0:
                    return page_size
            except ValueError:
                pass
        return self.max_page_size
