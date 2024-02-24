# Generated by Django 4.2.10 on 2024-02-24 16:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ambassadors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cost', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='MerchForSend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('comment', models.CharField(max_length=500)),
                ('shipped', models.BooleanField()),
                ('ambassador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merch_for_send', to='ambassadors.ambassadors', verbose_name='Амбассадор')),
                ('merch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merch_for_send', to='merch.merch', verbose_name='Мерч')),
            ],
        ),
    ]