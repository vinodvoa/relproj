# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='release',
            field=models.CharField(default='R4-2017', max_length=7),
            preserve_default=False,
        ),
    ]