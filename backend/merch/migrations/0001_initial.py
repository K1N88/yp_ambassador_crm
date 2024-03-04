# Generated by Django 4.2.10 on 2024-03-04 16:33

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
                ('count', models.IntegerField(default=1)),
                ('date', models.DateField(auto_now_add=True)),
                ('comment', models.CharField(max_length=500)),
                ('shipped', models.BooleanField()),
                ('ambassador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merch_for_send', to='ambassadors.ambassadors', verbose_name='Амбассадор')),
                ('merch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merch_for_send_items', to='merch.merch', verbose_name='Мерч')),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ambassador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ambassador', to='ambassadors.ambassadors')),
                ('merch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='budget_merch', to='merch.merchforsend')),
            ],
        ),
    ]
