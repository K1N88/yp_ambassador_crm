from django.conf import settings
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ambassadors.models import Ambassadors, Content, ContentType, StudyProgramm
from merch.models import Budget, MerchForSend
from users.models import CrmUser


class StudyProgrammSerializer(serializers.ModelSerializer):
    ''''Сериализатор для программ обучения'''

    class Meta:
        model = StudyProgramm
        fields = '__all__'


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
    study_programm = StudyProgrammSerializer()

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
    '''Сериализатор для обновления Контента.'''

    ambassadorName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContentType
        fields = ('ambassadorName', 'title', 'status')

    def get_ambassadorName(self, obj):
        ambassador = obj.ambassador
        return ambassador.full_name

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def validate(self, data):
        status_value = self.initial_data.get('status')
        title_status = self.initial_data.get('title')

        if status_value is None or title_status is None:
            raise serializers.ValidationError(
                'Необходимо указать `status` и `title` в теле запроса'
            )

        if title_status not in [
            item for sublist in ContentType.CONTENT_TYPES for item in sublist
        ]:
            raise serializers.ValidationError(
                'Укажите корректное значение `title`'
            )
        return data


class ContentSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели "Контент".'''

    class Meta:
        model = Content
        fields = ('id', 'link',)


class ContentTypeSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели "Тип Контента".'''
    contents = ContentSerializer(read_only=True, many=True)

    class Meta:
        model = ContentType
        fields = ('title', 'status', 'contents',)


class ContentListSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели "Контент" запроса GET(list).'''

    ambassadorName = serializers.SerializerMethodField(read_only=True)
    telegramHandle = serializers.CharField(
        source='telegram_handle', read_only=True
    )
    contentTypes = ContentTypeSerializer(
        source='content_types', many=True, read_only=True
    )

    class Meta:
        model = Ambassadors
        fields = ('ambassadorName', 'telegramHandle', 'contentTypes',)

    def get_ambassadorName(self, obj):
        return obj.full_name


class ContentPostSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели "Контент" запросов POST и DEL.'''

    ambassadorName = serializers.CharField(write_only=True)
    telegramHandle = serializers.CharField(write_only=True)
    is_guide = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = Content
        fields = ('ambassadorName', 'telegramHandle', 'link', 'is_guide',)

    def create(self, validated_data):
        name, surname = validated_data.get('ambassadorName').split()
        telegramHandle = validated_data.get('telegramHandle')
        link = validated_data.get('link')
        is_guide = validated_data.get('is_guide')

        try:
            ambassador = Ambassadors.objects.get(
                name=name,
                surname=surname,
                telegram_handle=telegramHandle
            )
        except Ambassadors.DoesNotExist:
            raise serializers.ValidationError(
                'Некорректное имя/фамилия/тг ссылка Амбассадора!'
            )

        # Количество всего контента амбассадора
        content_count = ambassador.content_types.annotate(
            total_content=Count('contents')
        ).aggregate(total=Sum('total_content'))['total'] or 0

        # Количество контента в Гайде амбассадора
        guide_content_count = ambassador.content_types.filter(
            title='Гайд'
        ).annotate(
            total_content=Count('contents')
        ).values_list('total_content', flat=True).first() or 0

        if content_count == 0:
            content_type_title = 'Первый отзыв'
        elif is_guide == 'Да' and guide_content_count >= 5:
            raise serializers.ValidationError(
                'Поле «Ссылки по гайду» может размещать только до пяти ссылок!'
            )
        elif is_guide == 'Да':
            content_type_title = 'Гайд'
        elif is_guide == 'Нет' or not is_guide:
            content_type_title = 'После гайда'
        else:
            raise serializers.ValidationError(
                'Поле «Это Гайд начинающего амбассадора?» может принимать ' +
                '`Да`, `Нет` или ``!'
            )

        content_type, _ = ContentType.objects.get_or_create(
            title=content_type_title,
            ambassador=ambassador,
        )

        content = Content.objects.create(
            link=link,
            content_type=content_type
        )

        return content

    def validate_ambassadorName(self, ambassadorName):
        """Проверка корректности ввода имени Амбассадора."""

        if len(ambassadorName.split()) != 2:
            raise serializers.ValidationError(
                "Введите `Имя` и `Фамилия` Амбассадора через пробел"
            )
        return ambassadorName
