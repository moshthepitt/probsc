from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import Http404

from core.mixins import CoreFormMixin
from scorecards.models import Scorecard, ScorecardKPI


class ScorecardKPIModalFormMixin(CoreFormMixin):
    """
    Common things for ScorecardKPI forms in modals
    """

    def get_initial(self):
        initial = super(ScorecardKPIModalFormMixin, self).get_initial()
        initial['scorecard'] = self.object.scorecard
        initial['kpi'] = self.object.kpi
        return initial

    def get_form_kwargs(self):
        kwargs = super(ScorecardKPIModalFormMixin, self).get_form_kwargs()
        kwargs['scorecard_kpi'] = self.object
        return kwargs


class ScorecardBelongsToUserMixin(object):
    """
    Used for objects with a scorecard field
    Ensures the scorecard belongs to the current user
    """

    def dispatch(self, *args, **kwargs):
        if self.get_object().scorecard.user != self.request.user:
            raise Http404
        return super(ScorecardBelongsToUserMixin, self).dispatch(*args, **kwargs)


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


class KPICreateMixin(object):
    """
    Adds KPI that was created to scorecard
    """

    def get_form_kwargs(self):
        kwargs = super(ScorecardFormMixin, self).get_form_kwargs()
        kwargs['scorecard'] = self.scorecard
        return kwargs

    def form_valid(self, form):
        redirect_url = super(ScorecardFormMixin, self).form_valid(form)
        ScorecardKPI.objects.create(kpi=self.object, scorecard=self.scorecard)
        return redirect_url
