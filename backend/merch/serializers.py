from rest_framework import serializers

from ambassadors.models import Ambassadors, ContentType
from .models import MerchForSend, Budget


class MerchSerializer(serializers.ModelSerializer):
    ambassadorName = serializers.CharField(source='ambassador.name', read_only=True)
    style = serializers.CharField(source='merch.name', read_only=True)
    commentToLogist = serializers.CharField(source='comment')
    kind = serializers.SerializerMethodField()
    requestDate = serializers.DateField(source='date')

    class Meta:
        model = MerchForSend
        fields = ('ambassadorName', 'id', 'style', 'commentToLogist',
                  'kind', 'requestDate',
                  'shipped')

    def get_kind(self, obj):
        content_type = obj.content_type
        return content_type.title
