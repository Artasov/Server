# Generated by Django 3.2.10 on 2022-01-28 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP_home', '0019_unconfirmeduser_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='guild',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]