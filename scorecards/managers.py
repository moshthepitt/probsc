from django.db.models import Manager

from core.managers import CoreManager


class ScorecardManager(CoreManager):

    pass


class ScorecardKPIManager(Manager):

    def get_queryset(self):
        queryset = super(ScorecardKPIManager, self).get_queryset()
        queryset = queryset.select_related('kpi', 'scorecard')
        return queryset


class ScoreKPIManager(Manager):

    def get_queryset(self):
        queryset = super(ScoreKPIManager, self).get_queryset()
        queryset = queryset.select_related('kpi', 'scorecard')
        return queryset
