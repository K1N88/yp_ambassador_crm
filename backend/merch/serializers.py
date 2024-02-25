from rest_framework import serializers

from ambassadors.models import Ambassadors, Budget
from .models import MerchForSend

class MerchSerializer(serializers.ModelSerializer):
    ambassadorName = serializers.CharField(source='ambassador.name')
    style = serializers.CharField(source='merch.name')
    commentToLogist = serializers.CharField(source='comment')
    kind = serializers.SerializerMethodField()
    requestDate = serializers.DateField(source='date')


    class Meta:
        model = MerchForSend
        fields = ('ambassadorName', 'id', 'style', 'commentToLogist', 'kind', 'requestDate',
                  'shipped')

    def get_kind(self, obj):
        pass

    def create(self, validated_data):
        ambassadorName = validated_data['ambassadorName']
        merch_for_send_id = validated_data['id']
        ambassador = Ambassadors.objects.get(name=ambassadorName)
        Budget.objects.create(ambassador=ambassador.id, merch=merch_for_send_id)

        return super().create(validated_data)
