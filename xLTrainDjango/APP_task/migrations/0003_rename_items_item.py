# Generated by Django 3.2.10 on 2022-03-16 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APP_task', '0002_alter_items_color'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Items',
            new_name='Item',
        ),
    ]