# Generated by Django 3.2.10 on 2022-01-27 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APP_shop', '0009_auto_20220127_0612'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlicense',
            old_name='xLGM_billid',
            new_name='billid',
        ),
        migrations.RemoveField(
            model_name='userlicense',
            name='xLUMRA_billid',
        ),
    ]