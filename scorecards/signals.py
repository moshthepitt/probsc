from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from scorecards.models import Score, ScorecardKPI, Scorecard
from scorecards.tasks import task_recalculate_scores


@receiver(post_save, sender=Score)
def calculate_score(sender, instance, created, **kwargs):
    score = instance
    try:
        scorecard_kpi = ScorecardKPI.objects.get(kpi=score.kpi,
                                                 scorecard=score.scorecard)
    except ScorecardKPI.DoesNotExist:
        pass
    else:
        scorecard_kpi.get_score(this_round=1, do_save=True)


@receiver(post_delete, sender=Score)
def recalculate_score(sender, instance, **kwargs):
    score = instance
    try:
        scorecard_kpi = ScorecardKPI.objects.get(kpi=score.kpi,
                                                 scorecard=score.scorecard)
    except ScorecardKPI.DoesNotExist:
        pass
    else:
        scorecard_kpi.get_score(this_round=1, do_save=True)


@receiver(post_save, sender=Scorecard)
def calculate_scorecard_score(sender, instance, created, **kwargs):
    """
    Recalculates all scores of the scorecard
    """
    scorecard = instance
    task_recalculate_scores.delay(scorecard_id=scorecard.id)
