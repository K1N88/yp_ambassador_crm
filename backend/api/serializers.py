from rest_framework import serializers

from ambassadors.models import Ambassadors, Content


class AmbassadorsSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Амбассадоров'''

    class Meta:
        model = Ambassadors
        fields = ('id', 'reg_date')


class ContentSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели "Контент" запросов POST PUT DEL.'''

    class Meta:
        model = Content
        fields = ('id',)


class ContentListSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели "Контент" запроса GET(list).'''

    class Meta:
        model = Content
        fields = ('ambassadorName', 'author', 'ingredients', 'is_favorited',)

