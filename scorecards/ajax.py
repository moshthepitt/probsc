from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from crispy_forms.utils import render_crispy_form

from .models import Scorecard
from .forms import InitiativeModalForm, ScoreModalForm


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
