# Generated by Django 3.2.10 on 2022-01-29 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP_home', '0021_auto_20220129_0458'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=1),
        ),
    ]
