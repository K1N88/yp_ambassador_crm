import pytest
from rest_framework import status
from django.test import RequestFactory

from api.views import AmbassadorsViewSet

EXPECTED_FILTEREST_FIELDS = ['study_programm', 'status', 'gender',
                           'country', 'city', 'want_to_do',
                           'date_from', 'date_to', 'supervisor']


@pytest.mark.django_db
class TestAmbassadorsView():
    AMBASSADORS_URL = '/api/ambassadors/'
    AMBASSADOR_DATA = {
        'surname': 'Пупкин',
        'name': 'Василий',
        'patronymic': 'Васильевич',
        'gender': 'М',
        'study_programm': None,
        'country': 'Россия',
        'city': 'Москва',
        'address': 'Пушкина, дом Колотушкина',
        'zip_code': '153000',
        'email': 'vasiliy@example.com',
        'phone': '88005553535',
        'telegram_handle': 'https://t.me/vasya',
        'education': 'Академия джедаев',
        'job': 'Джедай',
        'aim': 'Стать ситхом',
        'want_to_do': 'Ничего не хочу',
        'blog_url': 'http://89.111.174.233/swagger/',
        'shirt_size': 'M',
        'shoes_size': 42,
        'comment': 'Я Вася'
    }

    def test_create_ambassador(self, study_programme_obj, auth_client):
        self.AMBASSADOR_DATA['study_programm'] = study_programme_obj.id
        response = auth_client.post(self.AMBASSADORS_URL, self.AMBASSADOR_DATA)
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Убедитесь, что POST запрос на {self.AMBASSADORS_URL} с валидными данными возвращает статус 201'
        )

    def test_update_ambassador(self, auth_client, ambassadors_obj):
        self.AMBASSADOR_DATA['name'] = 'Невасилий'
        response_put = auth_client.put(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}/',
                                       self.AMBASSADOR_DATA)
        response_patch = auth_client.patch(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}/',
                                           data={'surname': 'Непупкин'})
        assert response_put.status_code == status.HTTP_200_OK, (
            f'Убедитесь, что PUT запрос на {self.AMBASSADORS_URL} возвращает статус 200'
        )
        assert response_patch.status_code == status.HTTP_200_OK, (
            f'Убедитесь, что PATCH запрос на {self.AMBASSADORS_URL} возвращает статус 200'
        )

    def test_list_ambassadors(self, auth_client):
        response = auth_client.get(self.AMBASSADORS_URL)
        assert response.status_code == status.HTTP_200_OK, (
            f'Убедитесь, что GET запрос на {self.AMBASSADORS_URL} возвращает статус 200'
        )

    def test_get_budget(self, ambassadors_obj, auth_client, budget_obj):
        response = auth_client.get(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}/budget/')
        assert response.status_code == status.HTTP_200_OK
        assert ambassadors_obj.id == budget_obj.ambassador.id, (
            f'Убедитесь, что GET запрос на {self.AMBASSADORS_URL}{ambassadors_obj.id}/budget/ возвращает статус 200'
        )

    def test_create_ambassador_with_invalid_data(self, study_programme_obj, auth_client):
        invalid_shoes_size_value = 100
        self.AMBASSADOR_DATA['study_programm'] = study_programme_obj.id
        self.AMBASSADOR_DATA['shoes_size'] = invalid_shoes_size_value
        response = auth_client.post(self.AMBASSADORS_URL, self.AMBASSADOR_DATA)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f'Убедитесь, что POST запрос на {self.AMBASSADORS_URL} с невалидными данными возвращает статус 400'
        )

    def test_delete_ambassador(self, ambassadors_obj, auth_client):
        response = auth_client.delete(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}/')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (
            f'Убедитесь, что DELETE запрос на {self.AMBASSADORS_URL} возвращает статус 405'
        )

    def test_filterset_fields_exists(self):
        AmbassadorsViewSet.request = RequestFactory().get(self.AMBASSADORS_URL)
        assert AmbassadorsViewSet.filterset_fields == EXPECTED_FILTEREST_FIELDS, (
            f'Убедитесь, что в представлении используются все необходимые поля для фильтрации: {EXPECTED_FILTEREST_FIELDS}'
        )
