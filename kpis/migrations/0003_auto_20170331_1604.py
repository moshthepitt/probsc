# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpis', '0002_auto_20170331_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpi',
            name='baseline',
            field=models.DecimalField(decimal_places=2, default=0, help_text='', max_digits=64, verbose_name='Base Line'),
        ),
    ]
