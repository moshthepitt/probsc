# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Scorecard, Evidence, Score, Initiative, ScorecardKPI


@admin.register(Scorecard)
class ScorecardAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'user',
        'active',
    )
    list_filter = ('user', 'customer', 'active')
    raw_id_fields = ('kpis', 'user', 'customer')
    search_fields = ('name',)


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'scorecard',
        'name',
        'date',
        'file',
    )
    list_filter = ('scorecard', 'date')
    raw_id_fields = ('scorecard', )
    search_fields = ('name',)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'scorecard',
        'kpi',
        'value',
        'review_round',
    )
    list_filter = ('date', 'scorecard', 'kpi')
    raw_id_fields = ('kpi', 'scorecard')


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'date',
        'scorecard',
        'kpi',
    )
    list_filter = ('date', 'scorecard', 'kpi')
    raw_id_fields = ('kpi', 'scorecard')
    search_fields = ('name',)


@admin.register(ScorecardKPI)
class ScorecardKPIAdmin(admin.ModelAdmin):
    list_display = ('id', 'scorecard', 'kpi', 'score')
    list_filter = ('scorecard', 'kpi')
    raw_id_fields = ('kpi', 'scorecard')
