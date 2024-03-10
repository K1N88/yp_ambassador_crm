import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ambassadors.models import (Ambassadors, StudyProgramm,
                                Content, ContentType)
from merch.models import Budget, Merch, MerchForSend
from users.models import CrmUser


@pytest.fixture
def study_programme_obj():
    return StudyProgramm.objects.create(title='Python-разработчик')


@pytest.fixture
def ambassadors_obj(study_programme_obj):
    return Ambassadors.objects.create(
        surname='Пупкин', name='Василий', patronymic='Васильевич', gender='М', study_programm=study_programme_obj,
        country='Россия', city='Москва', address='Пушкина, дом Колотушкина', zip_code='153000',
        email='vasiliy@example.com', phone='88005553535', telegram_handle='https://t.me/vasya',
        education='Академия джедаев', job='Джедай', aim='Стать ситхом',
        want_to_do='Ничего не хочу', shirt_size='M', shoes_size=42
      )


@pytest.fixture
def ambassadors_obj_2(study_programme_obj):
    return Ambassadors.objects.create(
        surname='Вупкин', name='Пасилий', patronymic='Пасильевич', gender='М', study_programm=study_programme_obj,
        country='Россия', city='Москва', address='Пушкина, дом Колотушкина', zip_code='153024',
        email='pasiliy@example.com', phone='88005553523', telegram_handle='https://t.me/pasya',
        education='Академия джедаев', job='Джедай', aim='Стать ситхом',
        want_to_do='Ничего не хочу', shirt_size='M', shoes_size=42
      )


@pytest.fixture
def content_type_obj(ambassadors_obj):
    return ContentType.objects.create(
        title='Первый отзыв',
        status='Не выполнено',
        ambassador=ambassadors_obj
    )


@pytest.fixture
def merch_obj():
    return Merch.objects.create(
        name='Футболка',
        cost=1000
    )


@pytest.fixture
def merch_for_send_obj(ambassadors_obj, merch_obj):
    return MerchForSend.objects.create(
        ambassador=ambassadors_obj,
        merch=merch_obj,
        count=1,
        comment='Коммент',
        shipped=True
    )


@pytest.fixture
def budget_obj(ambassadors_obj, merch_for_send_obj):
    return Budget.objects.create(
        ambassador=ambassadors_obj,
        merch=merch_for_send_obj
    )


@pytest.fixture
def user():
    return CrmUser.objects.create(
        username='Tester',
        name='Евгений',
        surname='Онегин',
        email='evgeniy@mail.ru',
        password='password',
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def token(user):
    return Token.objects.create(user=user)


@pytest.fixture
def content_obj(content_type_obj):
    return Content.objects.create(
        link='http://89.111.174.233/swagger/',
        content_type=content_type_obj,
    )
