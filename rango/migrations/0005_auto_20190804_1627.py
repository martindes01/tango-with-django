# Generated by Django 2.2.3 on 2019-08-04 15:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_auto_20190720_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='first_visit',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 4, 16, 27, 29, 322116)),
        ),
        migrations.AddField(
            model_name='page',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 4, 16, 27, 29, 322116)),
        ),
    ]
