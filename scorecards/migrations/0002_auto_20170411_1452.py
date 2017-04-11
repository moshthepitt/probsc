# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorecards', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scorecard',
            options={'ordering': ['-year', 'name'], 'verbose_name': 'Scorecard', 'verbose_name_plural': 'Scorecards'},
        ),
        migrations.AlterField(
            model_name='scorecard',
            name='name',
            field=models.TextField(max_length=255, verbose_name='Name'),
        ),
    ]
