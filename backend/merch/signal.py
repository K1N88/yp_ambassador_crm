from django.db.models.signals import post_save
from django.dispatch import receiver

from ambassadors.models import ContentType
from .models import MerchForSend

@receiver(post_save, sender=ContentType)
def create_merch_for_send(sender, instance, **kwargs):
    # Проверяем, было ли изменено поле status на "Выполнено"
    if instance.status == 'Выполнено':
        # Создаем объект MerchForSend
        MerchForSend.objects.create(
            ambassador=instance.ambassador,
            shipped=False
        )