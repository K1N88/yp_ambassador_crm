from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import MerchForSend
from .serializers import MerchSerializer
# from .filters import AmbassadorFilterBackend, MerchFilterBackend
from .filters import MerchFilter 


class MerchandiseView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = MerchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MerchFilter 

    def get_queryset(self):
        return MerchForSend.objects.all()

class SetStatusView(APIView):
    def put(self, request, ambassadorId, merchandiseId):
        instance = MerchForSend.objects.get(pk=merchandiseId)
        serializer = MerchSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
