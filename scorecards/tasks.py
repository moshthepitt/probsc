from .models import ScorecardKPI


def task_reclaculate_scores(customer_id=None):
    if customer_id:
        scorecard_kpis = ScorecardKPI.objects.filter(scorecard__customer__id=customer_id)
    else:
        scorecard_kpis = ScorecardKPI.objects.all()
    for scorecard_kpi in scorecard_kpis:
        scorecard_kpi.get_score(this_round=1, do_save=True)
