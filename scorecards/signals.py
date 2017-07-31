from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Score, ScorecardKPI


@receiver(post_save, sender=Score)
def calculate_score(sender, instance, created, **kwargs):
    score = instance
    try:
        scorecard_kpi = ScorecardKPI.objects.get(kpi=score.kpi, scorecard=score.scorecard)
    except ScorecardKPI.DoesNotExist:
        pass
    else:
        scorecard_kpi.get_score(this_round=1, do_save=True)
