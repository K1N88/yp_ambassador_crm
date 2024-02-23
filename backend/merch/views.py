from rest_framework import filters, mixins, status, viewsets
from .models import MerchForSend
from .serializers import MerchSerializer

class MerchandiseView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = MerchForSend.objects.all()
    serializer_class = MerchSerializer
