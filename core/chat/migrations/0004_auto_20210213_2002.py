# Generated by Django 3.1.1 on 2021-02-13 20:02

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20210213_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='icon',
            field=models.ImageField(blank=True, help_text='Group icon', upload_to=chat.models.group_icon_upload_location),
        ),
    ]