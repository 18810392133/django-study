# Generated by Django 2.0.2 on 2018-04-11 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userinfo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='photo',
            field=models.ImageField(blank=True, default='/static/images/2.PNG', upload_to=''),
        ),
    ]