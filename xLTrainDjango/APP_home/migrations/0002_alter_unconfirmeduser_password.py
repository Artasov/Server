# Generated by Django 3.2.10 on 2022-01-13 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP_home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unconfirmeduser',
            name='password',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
