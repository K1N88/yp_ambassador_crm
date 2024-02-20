from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings

from users.validators import validate_username


class CrmUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        max_length=settings.MAX_LENGTH,
        unique=True,
    )
    username = models.CharField(
        max_length=settings.MAX_LENGTH,
        unique=True,
        verbose_name='Логин пользователя',
        validators=[username_validator, validate_username],
    )
    first_name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Фамилия пользователя'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='email_user_unique',
                fields=['email', 'username'],
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
