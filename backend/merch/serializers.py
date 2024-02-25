from rest_framework import serializers

from .models import MerchForSend


class MerchSerializer(serializers.ModelSerializer):
    ambassadorName = serializers.CharField(source='ambassador.name')
    style = serializers.CharField(source='merch.name')
    commentToLogist = serializers.CharField(source='comment')
    kind = serializers.SerializerMethodField()
    requestDate = serializers.DateField(source='date')

    class Meta:
        model = MerchForSend
        fields = ('ambassadorName', 'id', 'style', 'commentToLogist',
                  'kind', 'requestDate',
                  'shipped')

    def get_kind(self, obj):
        # ambassador = obj.ambassador
        # content = ambassador.content_set.get()
        # kind = content.content_type.name
        # return kind
        return obj