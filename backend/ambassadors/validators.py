from django.core.exceptions import ValidationError


def validate_index(data):
    if not data.isnumeric() or len(data) < 6:
        raise ValidationError('Индекс должен состоять из 6 цифр!')
    return data


def validate_phone(data):
    if not data.isnumeric() or len(data) < 11:  # noqa
        raise ValidationError('Номер телефона должен состоять из 11 цифр!')  # noqa
    return data


def validate_tg_handle(data):
    if not data.lower().startswith("https://t.me/"):
        raise ValidationError('Ссылка на телеграм должна начинаться с "https://t.me/"!')  # noqa
    return data
