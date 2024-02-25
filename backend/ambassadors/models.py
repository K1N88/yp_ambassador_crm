from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from ambassadors.validators import (validate_index, validate_phone,
                                    validate_tg_handle)
from users.models import CrmUser


class StudyProgramm(models.Model):
    '''Программа обучения'''
    title = models.CharField(max_length=settings.MAX_LENGTH)

    def __str__(self):
        return self.title


class Ambassadors(models.Model):
    '''Амбассадоры'''

    GENDER = (
        ("М", "Мужской"),
        ("Ж", "Женский")
    )

    SHIRT_SIZES = (
        ("XS", "Extra Small"),
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large")
    )

    STATUS = (
        ("active", "Активный"),
        ("inactive", "Не активный")
    )
    CONTACT_PREFERENCES = (
        ("email", "email"),
        ("phone", "phone"),
        ("telegram", "telegram"),
    )

    date_created = models.DateField(verbose_name='дата регистрации',
                                    auto_now_add=True)

    # поля яндекс формы
    surname = models.CharField(verbose_name='фамилия',
                               max_length=settings.MAX_LENGTH)
    name = models.CharField(verbose_name='имя', max_length=settings.MAX_LENGTH)
    patronymic = models.CharField(verbose_name='отчество', null=True,
                                  max_length=settings.MAX_LENGTH)
    gender = models.CharField(max_length=1, choices=GENDER)
    study_programm = models.ForeignKey(StudyProgramm, null=True,
                                       on_delete=models.SET_NULL,
                                       related_name='ambassador_programm')
    country = models.CharField(max_length=settings.MAX_LENGTH)
    city = models.CharField(max_length=settings.MAX_LENGTH)
    address = models.CharField(max_length=settings.MAX_LENGTH)
    zip_code = models.CharField(max_length=6, validators=[validate_index])
    email = models.EmailField(max_length=settings.MAX_LENGTH, unique=True)
    phone = models.CharField(max_length=11, unique=True,
                             validators=[validate_phone])
    telegram_handle = models.CharField(max_length=settings.MAX_LENGTH,
                                       validators=[validate_tg_handle])
    education = models.CharField(max_length=settings.MAX_LENGTH)
    job = models.CharField(max_length=settings.MAX_LENGTH)
    aim = models.TextField()
    want_to_do = models.CharField(max_length=settings.MAX_LENGTH)
    blog_url = models.URLField(null=True, unique=True)
    shirt_size = models.CharField(max_length=2, choices=SHIRT_SIZES)
    shoes_size = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(10),
        MaxValueValidator(70)
    ])
    comment = models.TextField(null=True)

    # поля формы куратора
    promocode = models.CharField(null=True, max_length=settings.MAX_LENGTH)
    status = models.CharField(null=True, max_length=8, choices=STATUS)
    supervisor = models.ForeignKey(CrmUser, null=True,
                                   on_delete=models.SET_NULL,
                                   related_name='ambassador_user')
    supervisor_comment = models.TextField(null=True)
    contact_preferences = models.CharField(null=True, max_length=8,
                                           choices=CONTACT_PREFERENCES)

    class Meta:
        ordering = ('surname', 'name', 'patronymic', 'date_created')


class Content(models.Model):
    '''Контент.'''
    link = models.URLField()

    def __str__(self):
        return f"{self.link} for {self.ambassador.name}"


class ContentType(models.Model):
    '''Тип Контента.'''

    CONTENT_TYPES = [
        ('отзыв', 'Отзыв'),
        ('гайд', 'Гайд'),
        ('после_гайда', 'После гайда'),
    ]

    CONTENT_STATUS = [
        ('выполнено', 'Выполнено'),
        ('не_выполнено', 'Не выполнено'),
    ]

    title = models.CharField(
        max_length=15,
        verbose_name="Название контента",
        choices=CONTENT_TYPES
    )
    status = models.CharField(
        max_length=10,
        verbose_name="Статус контента",
        choices=CONTENT_STATUS
    )
    ambassador = models.ForeignKey(Ambassadors, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.ambassador.name}"