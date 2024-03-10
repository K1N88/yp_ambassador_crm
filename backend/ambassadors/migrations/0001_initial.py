# Generated by Django 4.2.10 on 2024-03-09 14:30

import ambassadors.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ambassadors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='дата регистрации')),
                ('surname', models.CharField(max_length=250, verbose_name='фамилия')),
                ('name', models.CharField(max_length=250, verbose_name='имя')),
                ('patronymic', models.CharField(blank=True, max_length=250, null=True, verbose_name='отчество')),
                ('gender', models.CharField(choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')], max_length=7)),
                ('country', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('zip_code', models.CharField(max_length=6, validators=[ambassadors.validators.validate_index])),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('phone', models.CharField(max_length=11, unique=True, validators=[ambassadors.validators.validate_phone])),
                ('telegram_handle', models.CharField(max_length=250, validators=[ambassadors.validators.validate_tg_handle])),
                ('education', models.CharField(max_length=250)),
                ('job', models.CharField(max_length=250)),
                ('aim', models.TextField()),
                ('want_to_do', models.CharField(max_length=250)),
                ('blog_url', models.URLField(null=True, unique=True)),
                ('shirt_size', models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], max_length=2)),
                ('shoes_size', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(70)])),
                ('comment', models.TextField(null=True)),
                ('promocode', models.CharField(max_length=250, null=True)),
                ('status', models.CharField(choices=[('active', 'Активный'), ('pause', 'На паузе'), ('not_ambassador', 'Не амбассадор'), ('to_check', 'Уточняется')], max_length=14, null=True)),
                ('supervisor_comment', models.TextField(null=True)),
                ('contact_preferences', models.CharField(choices=[('email', 'email'), ('phone', 'phone'), ('telegram', 'telegram')], max_length=8, null=True)),
            ],
            options={
                'ordering': ('surname', 'name', 'patronymic', 'date_created'),
            },
        ),
        migrations.CreateModel(
            name='StudyProgramm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Первый отзыв', 'Первый отзыв'), ('Гайд', 'Гайд'), ('После гайда', 'После гайда')], max_length=15, verbose_name='Название контента')),
                ('status', models.CharField(choices=[('Выполнено', 'Выполнено'), ('Не выполнено', 'Не выполнено')], default='Не выполнено', max_length=15, verbose_name='Статус контента')),
                ('ambassador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_types', to='ambassadors.ambassadors')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки контента')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='ambassadors.contenttype')),
            ],
        ),
        migrations.AddField(
            model_name='ambassadors',
            name='study_programm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ambassador_programm', to='ambassadors.studyprogramm'),
        ),
    ]
