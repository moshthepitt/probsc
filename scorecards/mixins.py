from django.shortcuts import get_object_or_404
from django.urls import reverse

from scorecards.models import Scorecard


class ScorecardMixin(object):
    """
    Adds scorecard to context
    """

    def get_context_data(self, **kwargs):
        context = super(ScorecardMixin, self).get_context_data(**kwargs)
        context['scorecard'] = self.scorecard
        return context

    def get_success_url(self):
        return reverse('scorecards:scorecards_kpis_list', args=[self.scorecard.pk])

    def dispatch(self, request, *args, **kwargs):
        self.scorecard = get_object_or_404(Scorecard, pk=kwargs.pop('scorecard_pk', None))
        return super(ScorecardMixin, self).dispatch(request, *args, **kwargs)


class ScorecardFormMixin(object):
    """
    Adds stuff for forms that have scorecard elements
    """

    def get_form_kwargs(self):
        kwargs = super(ScorecardFormMixin, self).get_form_kwargs()
        kwargs['scorecard'] = self.scorecard
        return kwargs
