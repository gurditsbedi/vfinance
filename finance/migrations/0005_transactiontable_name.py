# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-28 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_auto_20170127_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactiontable',
            name='name',
            field=models.CharField(default='zakhamBharna', max_length=128),
            preserve_default=False,
        ),
    ]
