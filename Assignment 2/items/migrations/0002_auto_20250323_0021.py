# Generated by Django 3.2.25 on 2025-03-23 00:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 1, 0, 0)),
        ),
        migrations.AlterField(
            model_name='items',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 1, 0, 0)),
        ),
    ]
