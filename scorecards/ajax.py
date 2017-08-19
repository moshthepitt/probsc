from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import ProtectedError

from crispy_forms.utils import render_crispy_form

from .models import Scorecard, Initiative, Score
from .forms import InitiativeModalForm, ScoreModalForm
from .access import can_access_scorecard


@csrf_exempt
def process_score_form(request):
    form = ScoreModalForm(request.POST or None)
    if form.is_valid():
        scorecard_pk = request.POST.get('scorecard')
        if scorecard_pk.isdigit():
            try:
                scorecard = Scorecard.objects.get(pk=int(scorecard_pk))
            except Scorecard.DoesNotExist:
                pass
            else:
                if request.user.userprofile.customer == scorecard.customer:
                    form.save()
                    return JsonResponse({
                        'success': True
                    })
    form_html = render_crispy_form(form)
    return JsonResponse({'success': False, 'form_html': form_html})


@csrf_exempt
def process_initiative_form(request):
    form = InitiativeModalForm(request.POST or None)
    if form.is_valid():
        scorecard_pk = request.POST.get('scorecard')
        if scorecard_pk.isdigit():
            try:
                scorecard = Scorecard.objects.get(pk=int(scorecard_pk))
            except Scorecard.DoesNotExist:
                pass
            else:
                if request.user.userprofile.customer == scorecard.customer:
                    form.save()
                    return JsonResponse({
                        'success': True
                    })
    form_html = render_crispy_form(form)
    return JsonResponse({'success': False, 'form_html': form_html})


@csrf_exempt
def delete_initiative(request, pk):
    try:
        initiative = Initiative.objects.get(pk=pk)
    except Initiative.DoesNotExist:
        return JsonResponse({'success': False})
    else:
        if (request.user.userprofile.customer == initiative.scorecard.customer)\
           and can_access_scorecard(initiative, request.user):
            try:
                initiative.delete()
            except ProtectedError:
                return JsonResponse({'success': False})
            else:
                return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@csrf_exempt
def delete_score(request, pk):
    try:
        score = Score.objects.get(pk=pk)
    except Score.DoesNotExist:
        return JsonResponse({'success': False})
    else:
        if (request.user.userprofile.customer == score.scorecard.customer)\
           and can_access_scorecard(score, request.user):
            try:
                score.delete()
            except ProtectedError:
                return JsonResponse({'success': False})
            else:
                return JsonResponse({'success': True})
    return JsonResponse({'success': False})
