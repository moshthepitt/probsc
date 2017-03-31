# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'financial_year_end_day',
        'financial_year_end_month',
        'review_rounds',
        'active',
    )
    list_filter = ('created',)
    search_fields = ('name',)
