# Generated by Django 3.2.10 on 2022-01-29 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APP_home', '0020_user_guild'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unconfirmeduser',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]
