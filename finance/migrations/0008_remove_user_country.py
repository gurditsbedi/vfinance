# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-02 18:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_user_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
    ]
