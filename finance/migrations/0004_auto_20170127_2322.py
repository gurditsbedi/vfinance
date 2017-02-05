# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-27 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20170126_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactiontable',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transactiontable',
            name='shares',
            field=models.IntegerField(),
        ),
    ]
