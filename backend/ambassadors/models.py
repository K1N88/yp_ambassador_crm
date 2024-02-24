from django.db import models


class Ambassadors(models.Model):
    '''Амбассадоры'''
    reg_date = models.DateField(verbose_name='дата регистрации',)

    class Meta:
        ordering = ('reg_date',)


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
