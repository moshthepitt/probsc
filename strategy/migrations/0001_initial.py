# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 07:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customers.Customer', verbose_name='Customer')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='strategy.Objective', verbose_name='Contributes to')),
            ],
            options={
                'verbose_name': 'Objective',
                'ordering': ['name', 'strategic_theme'],
                'verbose_name_plural': 'Objectives',
            },
        ),
        migrations.CreateModel(
            name='StrategicTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customers.Customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Strategic Theme',
                'ordering': ['name'],
                'verbose_name_plural': 'Strategic Themes',
            },
        ),
        migrations.AddField(
            model_name='objective',
            name='strategic_theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='strategy.StrategicTheme', verbose_name='Strategic Theme'),
        ),
    ]
