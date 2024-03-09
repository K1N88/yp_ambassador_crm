import pytest

from collections import OrderedDict

from .test_views import AMBASSADOR_DATA, CONTENT_DATA
from ambassadors.models import Ambassadors
from api.serializers import (AmbassadorSerializer, AmbassadorUpdateSerializer, AmbassadorPostSerializer,
                             SupervisorSerializer, StudyProgrammSerializer, BudgetSerializer,
                             ContentListSerializer, ContentPostSerializer, ContentSerializer,
                             ContentTypeSerializer, ContentUpdateSerializer)


@pytest.mark.django_db
class TestAmbassadorsSerializers():

    def test_post(self, study_programme_obj):
        AMBASSADOR_DATA['study_programm'] = study_programme_obj
        serializer =  AmbassadorPostSerializer(AMBASSADOR_DATA)
        expected_structure = {
            "surname": "Пупкин",
            "name": "Василий",
            "patronymic": "Васильевич",
            "gender": "М",
            "study_programm": 1,
            "country": "Россия",
            "city": "Москва",
            "address": "Пушкина, дом Колотушкина",
            "zip_code": "153000",
            "email": "vasiliy@example.com",
            "phone": "88005553535",
            "telegram_handle": "https://t.me/vasya",
            "education": "Академия джедаев",
            "job": "Джедай",
            "aim": "Стать ситхом",
            "want_to_do": "Ничего не хочу",
            "blog_url": "http://89.111.174.233/swagger/",
            "shirt_size": "M",
            "shoes_size": 42,
            "comment": "Я Вася"
        }
        assert serializer.data == expected_structure, (
            'Убедитесь, что ответ API соответствует ожидаемой структуре ответа'
        )
        assert serializer.is_valid, (
            f'Убедитесь, что {serializer} разрешает создать объект с валидными данными'
        )

    def test_get(self, study_programme_obj):
        ambassador_1_data = {
            "id": 1,
            "date_created": None,
            "surname": "Вупкин",
            "name": "Пасилий",
            "patronymic": "Пасильевич",
            "gender": "М",
            "country": "Россия",
            "city": "Москва",
            "address": "Пушкина, дом Колотушкина",
            "zip_code": "153024",
            "email": "pasiliy@example.com",
            "phone": "88005553523",
            "telegram_handle": "https://t.me/pasya",
            "education": "Академия джедаев",
            "job": "Джедай",
            "aim": "Стать ситхом",
            "want_to_do": "Ничего не хочу",
            "blog_url": None,
            "shirt_size": "M",
            "shoes_size": 42,
            "comment": None,
            "promocode": None,
            "status": None,
            "supervisor_comment": None,
            "contact_preferences": None,
            "study_programm": study_programme_obj,
            "supervisor": None
        }
        ambassador_2_data = {
            "id": 2,
            "date_created": None,
            "surname": "Пупкин",
            "name": "Василий",
            "patronymic": "Васильевич",
            "gender": "М",
            "country": "Россия",
            "city": "Москва",
            "address": "Пушкина, дом Колотушкина",
            "zip_code": "153000",
            "email": "vasiliy@example.com",
            "phone": "88005553535",
            "telegram_handle": "https://t.me/vasya",
            "education": "Академия джедаев",
            "job": "Джедай",
            "aim": "Стать ситхом",
            "want_to_do": "Ничего не хочу",
            "blog_url": None,
            "shirt_size": "M",
            "shoes_size": 42,
            "comment": None,
            "promocode": None,
            "status": None,
            "supervisor_comment": None,
            "contact_preferences": None,
            "study_programm": study_programme_obj,
            "supervisor": None
        }
        
        ambassador_1 = Ambassadors.objects.create(**ambassador_1_data)
        ambassador_2 = Ambassadors.objects.create(**ambassador_2_data)

        serializer = AmbassadorSerializer([ambassador_1, ambassador_2], many=True)
        serialized_data = serializer.data

        ambassador_1_data["date_created"] = ambassador_1.date_created.isoformat()
        ambassador_1_data["study_programm"] = 1
        ambassador_2_data["date_created"] = ambassador_2.date_created.isoformat()
        ambassador_2_data["study_programm"] = 2

        expected_structure = [
            OrderedDict(
                [('id', 1), ('date_created', '2024-03-09'), ('surname', 'Вупкин'),
                 ('name', 'Пасилий'), ('patronymic', 'Пасильевич'), ('gender', 'М'),
                 ('country', 'Россия'), ('city', 'Москва'), ('address', 'Пушкина, дом Колотушкина'),
                 ('zip_code', '153024'), ('email', 'pasiliy@example.com'), ('phone', '88005553523'),
                 ('telegram_handle', 'https://t.me/pasya'), ('education', 'Академия джедаев'),
                 ('job', 'Джедай'), ('aim', 'Стать ситхом'), ('want_to_do', 'Ничего не хочу'),
                 ('blog_url', None), ('shirt_size', 'M'), ('shoes_size', 42), ('comment', None),
                 ('promocode', None), ('status', None), ('supervisor_comment', None),
                 ('contact_preferences', None), ('study_programm', 1), ('supervisor', None)]
                ),
            OrderedDict(
                [('id', 2), ('date_created', '2024-03-09'), ('surname', 'Пупкин'),
                 ('name', 'Василий'), ('patronymic', 'Васильевич'), ('gender', 'М'),
                 ('country', 'Россия'), ('city', 'Москва'), ('address', 'Пушкина, дом Колотушкина'),
                 ('zip_code', '153000'), ('email', 'vasiliy@example.com'), ('phone', '88005553535'),
                 ('telegram_handle', 'https://t.me/vasya'), ('education', 'Академия джедаев'),
                 ('job', 'Джедай'), ('aim', 'Стать ситхом'), ('want_to_do', 'Ничего не хочу'),
                 ('blog_url', None), ('shirt_size', 'M'), ('shoes_size', 42), ('comment', None),
                 ('promocode', None), ('status', None), ('supervisor_comment', None),
                 ('contact_preferences', None), ('study_programm', 1), ('supervisor', None)]
                )
            ]

        assert serialized_data == expected_structure, (
            'Убедитесь, что ответ API соответствует ожидаемой структуре ответа'
        )

    def test_update(self, study_programme_obj):

        ambassador = Ambassadors.objects.create(
            surname='Иванов',
            name='Иван',
            gender='М',
            country='Россия',
            city='Москва',
            address='ул. Пушкина, д.10',
            zip_code='123456',
            email='ivanov@example.com',
            phone='88005553535',
            telegram_handle='https://t.me/ivanov',
            education='Высшее',
            job='Программист',
            aim='Получить новый опыт',
            want_to_do='Развиваться',
            shirt_size='M',
            shoes_size=42,
            study_programm=study_programme_obj
        )

        update_data = {
            'blog_url': 'https://example.com/blog',
            'promocode': '12345',
            'status': 'active',
            'supervisor': None,
            'supervisor_comment': 'Good job!',
            'contact_preferences': 'email'
        }

        serializer = AmbassadorUpdateSerializer(instance=ambassador, data=update_data, partial=True)
        assert serializer.is_valid()
        updated_ambassador = serializer.save()

        assert updated_ambassador.blog_url == 'https://example.com/blog', (
            'Убедитесь что при обновлении объекта Ambassdors содержимое поля "blog_url" '
            'содержит новые данные'
        )
        assert updated_ambassador.promocode == '12345', (
            'Убедитесь что при обновлении объекта Ambassdors содержимое поля "promocode" '
            'содержит новые данные'
        )
        assert updated_ambassador.status == 'active', (
            'Убедитесь что при обновлении объекта Ambassdors содержимое поля "status" '
            'содержит новые данные'
        )
        assert updated_ambassador.supervisor is None, (
            'Убедитесь что при обновлении объекта Ambassdors содержимое поля "supervisor" '
            'содержит новые данные'
        )
        assert updated_ambassador.supervisor_comment == 'Good job!', (
            'Убедитесь что при обновлении объекта Ambassdors содержимое поля "supervisor_comment" '
            'содержит новые данные'
        )
        assert updated_ambassador.contact_preferences == 'email', (
            'Убедитесь что при обновлении объекта Ambassdors содержимое поля "contact_preferences" '
            'содержит новые данные'
        )
