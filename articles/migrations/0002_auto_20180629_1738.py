# Generated by Django 2.0.2 on 2018-06-29 09:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='creat',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 29, 9, 38, 54, 375653, tzinfo=utc)),
        ),
    ]
