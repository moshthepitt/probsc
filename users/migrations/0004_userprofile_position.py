# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-03 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_department_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='position',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Position', verbose_name='job Position'),
        ),
    ]
