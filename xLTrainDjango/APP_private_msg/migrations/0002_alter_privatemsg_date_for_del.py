# Generated by Django 3.2.10 on 2022-04-08 00:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP_private_msg', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatemsg',
            name='date_for_del',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 8, 0, 40, 51, 195904)),
        ),
    ]