# Generated by Django 3.1.7 on 2022-01-08 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220108_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hallmanager',
            name='phone_number',
            field=models.CharField(default='03214123882', max_length=12),
        ),
    ]
