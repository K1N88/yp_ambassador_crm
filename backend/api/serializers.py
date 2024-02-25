from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import serializers

from ambassadors.models import Ambassadors, StudyProgramm, Content, ContentType
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


class ContentUpdateSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели "Контент" запросов PUT PATCH.'''

    class Meta:
        model = Content
        # fields = ('content_type',)
        fields = ('id',)


class ContentItemSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели "Контент" внутри ContentType.'''

    class Meta:
        model = Content
        fields = ('link', )


class ContentTypeSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели "Тип Контента" в ContentListSerializer.'''

    content = ContentItemSerializer(many=True, read_only=True)

    class Meta:
        model = ContentType
        fields = ('title', 'status', 'content')


class ContentListSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели "Контент" запроса GET(list).'''
    ambassadorName = serializers.CharField(source='content_type.ambassador.name')
    telegramHandle = serializers.CharField(source='content_type.ambassador.telegram_handle', read_only=True)
    # content_types = ContentTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        # fields = ('ambassadorName', 'telegramHandle', 'content_types',)
        fields = ('ambassadorName', 'telegramHandle')

    #FIXME

class ContentPostSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели "Контент" запроса POST.'''

    ambassadorName = serializers.CharField(write_only=True)
    telegramHandle = serializers.CharField(write_only=True)
    is_guide = serializers.BooleanField(write_only=True)

    class Meta:
        model = Content
        fields = ('ambassadorName', 'telegramHandle', 'link', 'is_guide')

    def create(self, validated_data):
        name, surname = validated_data.pop('ambassadorName').split()
        telegramHandle = validated_data.pop('telegramHandle')
        link = validated_data.pop('link')
        is_guide = validated_data.pop('is_guide')

        try:
            ambassador = Ambassadors.objects.get(
                name=name,
                surname=surname,
                telegram_handle=telegramHandle
            )
        except Ambassadors.DoesNotExist:
            raise serializers.ValidationError(
                f'Некорректное имя/фамилия/тг ссылка Амбассадора!'
            )

        is_first_content = ContentType.objects.filter(
            ambassador=ambassador).count() == 0

        if is_first_content:
            content_type_title = 'Первый отзыв'
        elif is_guide:
            content_type_title = 'Гайд'
        else:
            content_type_title = 'После гайда'

        content_type, _ = ContentType.objects.get_or_create(
            title=content_type_title,
            ambassador=ambassador,
        )

        content = Content.objects.create(
            link=link,
            content_type=content_type
        )

        return content


