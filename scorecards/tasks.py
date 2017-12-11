from celery.decorators import task

from scorecards.models import ScorecardKPI


@task(name="task_recalculate_scores", ignore_result=True)
def task_recalculate_scores(scorecard_id=None, kpi_id=None):
    if scorecard_id:
        scorecard_kpis = ScorecardKPI.objects.filter(
            scorecard__id=scorecard_id)
    elif kpi_id:
        scorecard_kpis = ScorecardKPI.objects.filter(
            kpi__id=kpi_id)
    else:
        scorecard_kpis = ScorecardKPI.objects.all()

    for scorecard_kpi in scorecard_kpis:
        scorecard_kpi.get_score(this_round=1, do_save=True)
