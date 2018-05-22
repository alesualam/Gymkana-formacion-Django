# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-22 16:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20180522_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='image',
            field=models.ImageField(default='images/image.jpg', upload_to='images/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png'])]),
        ),
    ]