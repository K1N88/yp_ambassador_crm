from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _, ngettext  # noqa


def validate_username(data):
    if data.lower() == 'me':
        raise ValidationError('Имя "me" не использовать!')
    return data
