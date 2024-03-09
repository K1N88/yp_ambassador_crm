import pytest
from rest_framework import status
from django.test import RequestFactory

from api.views import AmbassadorsViewSet, BudgetViewSet

EXPECTED_FILTEREST_FIELDS = ['study_programm', 'status', 'gender',
                           'country', 'city', 'want_to_do',
                           'date_from', 'date_to', 'supervisor']
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
CONTENT_DATA = {
        'ambassadorName': 'Василий Пупкин',
        'telegramHandle': 'https://t.me/vasya',
        'link': 'http://89.111.174.233/swagger/',
        'is_guide': True
    }


@pytest.mark.django_db
class TestAmbassadorsView():
    AMBASSADORS_URL = '/api/ambassadors/'
    CONTENT_TYPE_DATA = {
        'title': 'Первый отзыв',
        'status': 'Выполнено',
        'ambassador': None
    }

    def test_create_ambassador(self, study_programme_obj, auth_client):
        AMBASSADOR_DATA['study_programm'] = study_programme_obj.id
        response = auth_client.post(self.AMBASSADORS_URL, AMBASSADOR_DATA)
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Убедитесь, что POST запрос на {self.AMBASSADORS_URL} '
            'с валидными данными возвращает статус 201'
        )

    def test_update_ambassador(self, auth_client, ambassadors_obj):
        AMBASSADOR_DATA['name'] = 'Невасилий'
        response_put = auth_client.put(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}/',
                                       AMBASSADOR_DATA)
        response_patch = auth_client.patch(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}/',
                                           data={'surname': 'Непупкин'})
        assert response_put.status_code == status.HTTP_200_OK, (
            f'Убедитесь, что PUT запрос с валидными данными на '
            f'{self.AMBASSADORS_URL} возвращает статус 200'
        )
        assert response_patch.status_code == status.HTTP_200_OK, (
            f'Убедитесь, что PATCH запрос с валидными данными на '
            f'{self.AMBASSADORS_URL} возвращает статус 200'
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
            f'Убедитесь, что GET запрос на {self.AMBASSADORS_URL}'
            f'{ambassadors_obj.id}/budget/ dвозвращает статус 200'
        )

    def test_update_content(self, ambassadors_obj, auth_client, content_type_obj):
        self.CONTENT_TYPE_DATA['ambassador'] = ambassadors_obj
        response = auth_client.put(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}/contentStatus/',
                                   self.CONTENT_TYPE_DATA)
        assert response.status_code == status.HTTP_200_OK, (
            f'Убедитесь, что UPDATE запрос с валидными данными на '
            f'{self.AMBASSADORS_URL}{ambassadors_obj.id}/contentStatus/ возвращает статус 200'
        )

#    def test_delete_content(self, ambassadors_obj, auth_client, content_type_obj):
#        self.CONTENT_TYPE_DATA['ambassador'] = ambassadors_obj
#        response = auth_client.delete(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}'
#                                   f'/content/{content_type_obj.id}')
#        assert response.status_code == status.HTTP_301_MOVED_PERMANENTLY, (
#            f'Убедитесь, что DELETE запрос на {self.AMBASSADORS_URL}{ambassadors_obj.id}'
#            f'/content/{content_type_obj.id} возвращает 204'
#        )

    def test_filterset_fields_exists(self):
        AmbassadorsViewSet.request = RequestFactory().get(self.AMBASSADORS_URL)
        assert AmbassadorsViewSet.filterset_fields == EXPECTED_FILTEREST_FIELDS, (
            f'Убедитесь, что в представлении используются '
            f'все необходимые поля для фильтрации: {EXPECTED_FILTEREST_FIELDS}'
        )

    def test_create_ambassador_with_invalid_data(self, study_programme_obj, auth_client):
        invalid_shoes_size_value = 100
        AMBASSADOR_DATA['study_programm'] = study_programme_obj.id
        AMBASSADOR_DATA['shoes_size'] = invalid_shoes_size_value
        response = auth_client.post(self.AMBASSADORS_URL, AMBASSADOR_DATA)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f'Убедитесь, что POST запрос на {self.AMBASSADORS_URL} '
            'с невалидными данными возвращает статус 400'
        )

    def test_create_ambassador_withou_required_filed(self, auth_client):
        for field in list(AMBASSADOR_DATA.keys()):
            required_field = AMBASSADOR_DATA[field]
            AMBASSADOR_DATA[field] = ''
            response = auth_client.post(self.AMBASSADORS_URL, AMBASSADOR_DATA)
            assert response.status_code == status.HTTP_400_BAD_REQUEST, (
                f'Убедитесь, что при создании нового амбассадора поле "{field}" '
                f'является обязательным'
            )
            AMBASSADOR_DATA[field] = required_field

    def test_delete_ambassador(self, ambassadors_obj, auth_client):
        response = auth_client.delete(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}/')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (
            f'Убедитесь, что DELETE запрос на {self.AMBASSADORS_URL} возвращает статус 405'
        )

    def test_update_not_exists_content(self, ambassadors_obj, auth_client, content_type_obj):
        response = auth_client.put(f'{self.AMBASSADORS_URL}2/contentStatus/',
                                   self.CONTENT_TYPE_DATA)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            'Убедитесь, что запрос к несуществующему амбассадору возвращает 404'
        )

#    def test_delete_content(self, ambassadors_obj, auth_client, content_type_obj):
#        self.CONTENT_TYPE_DATA['ambassador'] = ambassadors_obj
#        response = auth_client.delete(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}'
#                                   f'/content/100')
#        assert response.status_code == status.HTTP_404_NOT_FOUND, (
#            f'Убедитесь, что DELETE запрос на {self.AMBASSADORS_URL}{ambassadors_obj.id} '
#            f'с несуществующим контентом возвращает 404'
#        )

    def test_get_content(self, auth_client, ambassadors_obj, content_type_obj):
        response = auth_client.get(f'{self.AMBASSADORS_URL}{ambassadors_obj.id}'
                                    f'/content/{content_type_obj.id}', follow=True)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (
            f'Убедитесь, что GET запрос на {self.AMBASSADORS_URL}{ambassadors_obj.id}'
            f'/content/{content_type_obj.id} возвращает 405'
        )


@pytest.mark.django_db
class TestStudyProgrammView():
    STUDY_PROGRAMM_URL = '/api/study_programms/'

    def test_get_list_study_programms(self, auth_client):
        response = auth_client.get(self.STUDY_PROGRAMM_URL)
        assert response.status_code == status.HTTP_200_OK, (
            f'Убедитесь, что GET запрос на {self.STUDY_PROGRAMM_URL} возвращает статус 200'
        )

    def test_get_study_programms_obj(self, auth_client, study_programme_obj):
        response_get_obj = auth_client.get(f'{self.STUDY_PROGRAMM_URL}{study_programme_obj.id}')
        assert response_get_obj.status_code == status.HTTP_404_NOT_FOUND, (
            f'Убедитесь, что GET запрос на {self.STUDY_PROGRAMM_URL}{study_programme_obj.id} '
            f'возвращает статус 404'
        )


@pytest.mark.django_db
class TestSupervisorView():
    SUPERVISOR_URL = '/api/supervisors/'

    def test_get_list_supervisors(self, auth_client):
        response = auth_client.get(self.SUPERVISOR_URL)
        assert response.status_code == status.HTTP_200_OK, (
            f'Убедитесь, что GET запрос на {self.SUPERVISOR_URL} возвращает статус 200'
        )

    def test_get_supervisors_obj(self, auth_client, user):
        response_get_obj = auth_client.get(f'{self.SUPERVISOR_URL}{user.id}')
        assert response_get_obj.status_code == status.HTTP_404_NOT_FOUND, (
            f'Убедитесь, что GET запрос на {self.SUPERVISOR_URL}{user.id} '
            f'возвращает статус 404'
        )


@pytest.mark.django_db
class TestBudget():
    BUDGET_URL = '/api/budget/'

    def test_get_list_budget(self, auth_client):
        response = auth_client.get(self.BUDGET_URL)
        assert response.status_code == status.HTTP_200_OK, (
            f'Убедитесь, что GET запрос на {self.BUDGET_URL} возвращает статус 200'
        )

    def test_get_budget_obj(self, auth_client, budget_obj):
        response_get_obj = auth_client.get(f'{self.BUDGET_URL}{budget_obj.id}')
        assert response_get_obj.status_code == status.HTTP_404_NOT_FOUND, (
            f'Убедитесь, что GET запрос на {self.BUDGET_URL}{budget_obj.id} '
            f'возвращает статус 404'
        )

    def test_get_excel(self, token):
        request_factory = RequestFactory()
        request = request_factory.get(f'{self.BUDGET_URL}excel/')
        request.META['HTTP_AUTHORIZATION'] = f'Token {token.key}'
        response = BudgetViewSet.as_view({'get': 'excel'})(request)
        
        assert response.status_code == status.HTTP_200_OK, (
           f'Убедитесь, что GET запрос на {self.BUDGET_URL}excel/ '
           f'возвращает статус 200'
        )
        assert response['Content-Type'] == 'application/ms-excel', (
            f'Убедитесь, что GET запрос на {self.BUDGET_URL}excel/ '
            f'возвращает файл типа Excel'
        )
        assert 'attachment; filename="budget.xls"' in response['Content-Disposition'], (
            f'Убедитесь, что GET запрос на {self.BUDGET_URL}excel/ '
            f'возвращает файл с названием "budget.xls"'
        )


@pytest.mark.django_db
class TestContentView():
    CONTENT_URL = '/api/content/'

    def test_get_list_content(self, auth_client, content_obj):
        response = auth_client.get(self.CONTENT_URL)
        assert response.status_code == status.HTTP_200_OK, (
            f'Убедитесь, что GET запрос на {self.CONTENT_URL} возвращает статус 200'
        )

    def test_create_content(self, auth_client, ambassadors_obj):
        response = auth_client.post(self.CONTENT_URL, CONTENT_DATA)
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Убедитесь, что POST запрос на {self.CONTENT_URL} '
            f'с валидными данными возвращает статус 201'
        )

    def test_create_content_with_invalid_data(self, auth_client, ambassadors_obj):
        CONTENT_DATA['link'] = 'Просто строка'
        response = auth_client.post(self.CONTENT_URL, CONTENT_DATA)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f'Убедитесь, что POST запрос на {self.CONTENT_URL} '
            f'с невалидными данными возвращает статус 400'
        )

    def test_create_content_with_not_exists_ambassador(self, auth_client, ambassadors_obj):
        CONTENT_DATA['ambassadorName'] = 'Ваня Иванов'
        response = auth_client.post(self.CONTENT_URL, CONTENT_DATA)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f'Убедитесь, что POST запрос на {self.CONTENT_URL} '
            f'с несуществущими именем и фамилией/ссылкой на ТГ возвращает статус 400'
        )

    def test_create_content_withou_required_filed(self, auth_client):
        for field in list(CONTENT_DATA.keys()):
            required_field = CONTENT_DATA[field]
            CONTENT_DATA[field] = ''
            response = auth_client.post(self.CONTENT_URL, CONTENT_DATA)
            assert response.status_code == status.HTTP_400_BAD_REQUEST, (
                f'Убедитесь, что при создании нового амбассадора поле "{field}" '
                f'является обязательным'
            )
            CONTENT_DATA[field] = required_field

    def test_get_content_obj(self, auth_client, content_obj):
        response = auth_client.get(f'{self.CONTENT_URL}{content_obj.id}')
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            f'Убедитесь, что GET запрос на {self.CONTENT_URL}{content_obj.id} '
            f'возвращает статус 404'
        )
