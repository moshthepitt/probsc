from django.utils.translation import ugettext as _
from django.urls import reverse, reverse_lazy
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib import messages

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView

from scorecards.mixins import ScorecardMixin, ScorecardFormMixin, KPICreateMixin
from scorecards.models import ScorecardKPI, Score
from .tables import KPITable, ScorecardKPITable
from .forms import KPIForm
from .models import KPI


class KPIListview(CoreListView):
    model = KPI
    table_class = KPITable
    search_fields = ['name', 'measure', 'description']

    def get_context_data(self, **kwargs):
        context = super(KPIListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('kpis:kpis_add')
        context['list_view_url'] = reverse_lazy('kpis:kpis_list')
        return context


class ScorecardKPIListview(ScorecardMixin, KPIListview):
    template_name = "scorecards/kpis_list.html"
    table_class = ScorecardKPITable

    def get_table_kwargs(self):
        kwargs = super(ScorecardKPIListview, self).get_table_kwargs()
        kwargs['scorecard'] = self.scorecard
        return kwargs

    def get_queryset(self):
        queryset = super(ScorecardKPIListview, self).get_queryset()
        return queryset.filter(scorecard=self.scorecard)

    def get_context_data(self, **kwargs):
        context = super(ScorecardKPIListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy(
            'scorecards:scorecards_kpis_add', args=[self.scorecard.pk])
        context['list_view_url'] = reverse_lazy(
            'scorecards:scorecards_kpis_list', args=[self.scorecard.pk])
        return context


class AddKPI(CoreCreateView):
    model = KPI
    form_class = KPIForm


class EditKPI(CoreUpdateView):
    model = KPI
    form_class = KPIForm


class DeleteKPI(CoreDeleteView):
    model = KPI
    success_url = reverse_lazy('kpis:kpis_list')


class AddScorecardKPI(KPICreateMixin, ScorecardFormMixin, ScorecardMixin, CoreCreateView):
    model = KPI
    form_class = KPIForm
    template_name = "scorecards/kpis_create.html"


class EditScorecardKPI(ScorecardFormMixin, ScorecardMixin, CoreUpdateView):
    model = KPI
    form_class = KPIForm
    template_name = "scorecards/kpis_edit.html"


class DeleteScorecardKPI(ScorecardMixin, CoreDeleteView):
    model = KPI
    template_name = "scorecards/kpis_delete.html"

    def delete(self, request, *args, **kwargs):
        try:
            scorecard_kpi = ScorecardKPI.objects.get(kpi=self.get_object(), scorecard=self.scorecard)
        except ScorecardKPI.DoesNotExist:
            info = _("An error occurred.")
            messages.error(request, info, fail_silently=True)
            return redirect(
                reverse(
                    'scorecards:scorecards_kpis_list', args=[self.scorecard.pk]
                )
            )
        else:
            scorecard_scores = Score.objects.filter(kpi=self.get_object())
            if not scorecard_scores:
                scorecard_kpi.delete()
            try:
                return super(CoreDeleteView, self).delete(request, *args, **kwargs)
            except ProtectedError:
                info = _("You cannot delete this item, it is referenced by other items.")
                messages.error(request, info, fail_silently=True)
                return redirect(
                    reverse(
                        'scorecards:scorecards_kpis_delete', args=[self.object.pk, self.scorecard.pk]
                    )
                )
