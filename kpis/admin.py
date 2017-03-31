# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import KPI


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'objective',
        'name',
        'measure',
        'perspective',
        'baseline',
        'target',
        'unit',
        'direction',
        'weight',
        'reporting_period',
        'calculation',
        'reporting_method',
        'active',
    )
    list_filter = ('objective', 'customer', 'active')
    raw_id_fields = ['objective', 'customer']
    search_fields = ('name',)
