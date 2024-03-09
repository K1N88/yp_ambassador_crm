from django.db import models
from django.core.validators import MinValueValidator
from ambassadors.models import Ambassadors

from backend.settings import NAME_MAX_LENGTH, COMMENT_MAX_LENGTH


class Merch(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    cost = models.IntegerField(validators=[MinValueValidator(1),])


class MerchForSend(models.Model):
    ambassador = models.ForeignKey(Ambassadors, on_delete=models.CASCADE,
                                   related_name='merch_for_send',
                                   verbose_name='Амбассадор')
    merch = models.ForeignKey(Merch, on_delete=models.CASCADE,
                              null=True,
                              related_name='merch_for_send_items',
                              verbose_name='Мерч')
    count = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=COMMENT_MAX_LENGTH)
    shipped = models.BooleanField()


class Budget(models.Model):
    ambassador = models.ForeignKey(
        Ambassadors, on_delete=models.CASCADE,
        blank=True, null=True, related_name='ambassador'
    )
    merch = models.ForeignKey(
        MerchForSend, on_delete=models.CASCADE,
        blank=True, null=True, related_name='budget_merch'
    )

    class Meta:
        ordering = ('ambassador',)
