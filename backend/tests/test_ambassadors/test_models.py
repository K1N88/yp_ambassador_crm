import pytest
from mixer.backend.django import mixer
# from django.core.exceptions import ValidationError

from ambassadors.models import Ambassadors, StudyProgramm


@pytest.mark.django_db
class TestStudyProgrammModel:

   def test_create_study_programm_with_valid_data(self):
      title = 'Python-разработчик'
      study_programm = StudyProgramm.objects.create(title=title)
      assert study_programm.title == title

   def test_str_method(self):
      title = 'Python-разработчик'
      study_programm = StudyProgramm.objects.create(title=title)
      assert str(study_programm) == title

   def test_relationship_with_other_models(self):
      study_programm = mixer.blend(StudyProgramm)
      ambassador = mixer.blend(Ambassadors, study_programm=study_programm)
      assert ambassador.study_programm == study_programm

   #def test_create_study_programm_with_invalid_data(self):
   #   with pytest.raises(ValidationError):
   #      StudyProgramm.objects.create(title='a' * 256)

   # не проходит валидация моделью

@pytest.mark.django_db
class TestAmbassadorsModel():

   def test_create_ambassador_with_valid_data(self):
      program = StudyProgramm.objects.create(title='Python-разработчик')
      ambassador = Ambassadors.objects.create(
         surname='Пупкин', name='Василий', gender='М', study_programm=program,
         country='Россия', city='Москва', address='Пушкина, дом Колотушкина', zip_code='153000',
         email='vasiliy@example.com', phone='88005553535', telegram_handle='https://t.me/vasya',
         education='Академия джедаев', job='Джедай', aim='Стать ситхом',
         want_to_do='Ничего не хочу', shirt_size='M', shoes_size=42
      )
      assert ambassador.pk is not None

   def test_study_programm_ambassador_relationship(self):
      program = StudyProgramm.objects.create(title='Python-разработчик')
      ambassador = Ambassadors.objects.create(
         surname='Пупкин', name='Василий', gender='М', study_programm=program,
         country='Россия', city='Москва', address='Пушкина, дом Колотушкина', zip_code='153000',
         email='vasiliy@example.com', phone='88005553535', telegram_handle='https://t.me/vasya',
         education='Академия джедаев', job='Джедай', aim='Стать ситхом',
         want_to_do='Ничего не хочу', shirt_size='M', shoes_size=42
      )
      assert ambassador.study_programm == program

#@pytest.mark.django_db
#def test_create_ambassador_with_invalid_data():
#   with pytest.raises(ValidationError):
#      Ambassadors.objects.create(
#         surname='Пупкин', name='Василий', gender='A', # Invalid gender
#         country='Россия', city='Москва', address='Пушкина, дом Колотушкина', zip_code='153000',
#         email='vasiliy@example.com', phone='88005553535', telegram_handle='https://t.me/vasya',
#         education='Академия джедаев', job='Джедай', aim='Стать ситхом',
#         want_to_do='Ничего не хочу', shirt_size='M', shoes_size=42
#      )

# не проходит валидация моделью
