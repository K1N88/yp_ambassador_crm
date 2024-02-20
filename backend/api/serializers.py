from rest_framework import serializers

from ambassadors.models import Ambassadors


class AmbassadorsSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Амбассадоров'''

    class Meta:
        model = Ambassadors
        fields = ('id', 'reg_date')
