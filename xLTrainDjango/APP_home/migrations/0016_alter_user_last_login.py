# Generated by Django 3.2.10 on 2022-01-27 23:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP_home', '0015_alter_user_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]