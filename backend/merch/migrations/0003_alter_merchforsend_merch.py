# Generated by Django 4.2.10 on 2024-03-02 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merch', '0002_alter_merchforsend_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchforsend',
            name='merch',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='merch_for_send_items', to='merch.merch', verbose_name='Мерч'),
        ),
    ]