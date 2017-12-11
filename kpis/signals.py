from django.db.models.signals import post_save
from django.dispatch import receiver

from kpis.models import KPI
from scorecards.tasks import task_recalculate_scores


@receiver(post_save, sender=KPI)
def calculate_kpi_scorecard_score(sender, instance, created, **kwargs):
    """
    Recalculates all scores of the scorecard
    """
    kpi = instance
    task_recalculate_scores.delay(kpi_id=kpi.id)
