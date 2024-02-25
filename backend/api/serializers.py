from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import serializers

from ambassadors.models import Ambassadors
from merch.models import MerchForSend, Budget


class AmbassadorsSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Амбассадоров'''
    surname = serializers.CharField(max_length=settings.MAX_LENGTH)
    name = serializers.CharField(max_length=settings.MAX_LENGTH)
    patronymic = serializers.CharField(max_length=settings.MAX_LENGTH)
    gender = serializers.CharField(max_length=1)
    study_programm = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='ambassador_programm'
    )
    country = serializers.CharField(max_length=settings.MAX_LENGTH)
    city = serializers.CharField(max_length=settings.MAX_LENGTH)
    address = serializers.CharField(max_length=settings.MAX_LENGTH)
    zip_code = serializers.CharField(max_length=6)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=12)
    telegram_handle = serializers.CharField(max_length=settings.MAX_LENGTH)
    education = serializers.CharField(max_length=settings.MAX_LENGTH)
    job = serializers.CharField(max_length=settings.MAX_LENGTH)
    aim = serializers.CharField()
    want_to_do = serializers.CharField(max_length=settings.MAX_LENGTH)
    blog_url = serializers.URLField(allow_blank=True)
    shirt_size = serializers.CharField(max_length=settings.MAX_LENGTH)
    shoes_size = serializers.IntegerField(min_value=10, max_value=70)
    comment = serializers.CharField(allow_blank=True)

    class Meta:
        model = Ambassadors
        fields = ('surname', 'name', 'patronymic', 'gender', 'study_programm',
                  'country', 'city', 'address', 'zip_code', 'email', 'phone',
                  'telegram_handle', 'education', 'job', 'aim', 'want_to_do',
                  'blog_url', 'shirt_size', 'shoes_size', 'comment')


class BudgetSerializer(serializers.Serializer):
    ambassadorName = serializers.CharField(
        source='ambassador.name', read_only=True
    )
    period = serializers.DateField(
        source='merch.date', read_only=True
    )
    style = serializers.CharField(
        source='merch.merch.name'
    )
    price = serializers.IntegerField(
        source='merch.merch.cost'
    )
    sum = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ('ambassadorName', 'period', 'style', 'price', 'sum')

    def get_sum(self, obj):
        merch_for_send = MerchForSend.objects.filter(ambassador=obj.ambassador)
        sum = 0

        for merch in merch_for_send:
            sum += merch.merch.cost

        return sum
