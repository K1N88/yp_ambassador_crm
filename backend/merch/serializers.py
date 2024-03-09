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


    def create(self, validated_data):
        ambassadorName = validated_data['ambassadorName']
        merch_for_send_id = validated_data['id']
        ambassador = Ambassadors.objects.get(name=ambassadorName)
        Budget.objects.create(ambassador=ambassador.id,
                              merch=merch_for_send_id)
        return super().create(validated_data)
