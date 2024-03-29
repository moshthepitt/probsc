# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 13:07
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.manager
import django_extensions.db.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email Address')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=255, verbose_name='Phone Number')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('financial_year_end_day', models.PositiveSmallIntegerField(default=31, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)], verbose_name='Financial Year End Day')),
                ('financial_year_end_month', models.PositiveSmallIntegerField(default=12, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Financial Year End Month')),
                ('review_rounds', models.PositiveSmallIntegerField(default=2, help_text='How many times is each scorecard reviewed? e.g. self review, supervisor review, etc', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Rounds of Review')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Customer',
                'ordering': ['name'],
                'verbose_name_plural': 'Customers',
            },
            managers=[
                ('objecs', django.db.models.manager.Manager()),
            ],
        ),
    ]
