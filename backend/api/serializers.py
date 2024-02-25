from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import serializers

from ambassadors.models import Ambassadors, StudyProgramm
from users.models import CrmUser
from merch.models import MerchForSend, Budget


class AmbassadorPostSerializer(serializers.ModelSerializer):
    ''''Сериализатор для создания Амбассадора'''

    class Meta:
        model = Ambassadors
        fields = ('surname', 'name', 'patronymic', 'gender', 'study_programm',
                  'country', 'city', 'address', 'zip_code', 'email', 'phone',
                  'telegram_handle', 'education', 'job', 'aim', 'want_to_do',
                  'blog_url', 'shirt_size', 'shoes_size', 'comment')


class AmbassadorSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Амбассадоров'''

    class Meta:
        model = Ambassadors
        fields = '__all__'


class AmbassadorUpdateSerializer(serializers.ModelSerializer):
    ''''Сериализатор для обновления Амбассадора'''

    class Meta:
        model = Ambassadors
        fields = ('blog_url', 'promocode', 'status', 'supervisor',
                  'supervisor_comment', 'contact_preferences')


class SupervisorSerializer(serializers.ModelSerializer):
    ''''Сериализатор для Кураторов'''

    class Meta:
        model = CrmUser
        fields = ('id', 'name', 'username', 'surname', 'email')


class StudyProgrammSerializer(serializers.ModelSerializer):
    ''''Сериализатор для программ обучения'''

    class Meta:
        model = StudyProgramm
        fields = '__all__'


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
