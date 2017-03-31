# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import StrategicTheme, Objective


@admin.register(StrategicTheme)
class StrategicThemeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'active',
    )
    list_filter = ('created', 'modified', 'customer', 'active')
    search_fields = ('name',)


@admin.register(Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'strategic_theme',
        'parent',
        'active',
    )
    list_filter = (
        'strategic_theme',
        'parent',
        'customer',
        'active',
    )
    search_fields = ('name',)
    raw_id_fields = ('parent', 'strategic_theme', 'customer')
