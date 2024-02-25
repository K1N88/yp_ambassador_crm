from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MerchForSend
from .serializers import MerchSerializer
from .filters import AmbassadorFilterBackend, MerchFilterBackend


class MerchandiseView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = MerchSerializer
    filter_backends = [AmbassadorFilterBackend, MerchFilterBackend]

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
