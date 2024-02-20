from django.db import models


class Ambassadors(models.Model):
    '''Амбассадоры'''
    reg_date = models.DateField(verbose_name='дата регистрации',)

    class Meta:
        ordering = ('reg_date',)
