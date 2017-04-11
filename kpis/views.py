from django.urls import reverse_lazy

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView

from scorecards.mixins import ScorecardMixin
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
        context['create_view_url'] = reverse_lazy('scorecards:scorecards_kpis_add', args=[self.scorecard.pk])
        context['list_view_url'] = reverse_lazy('scorecards:scorecards_kpis_list', args=[self.scorecard.pk])
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


class AddScorecardKPI(ScorecardMixin, CoreCreateView):
    model = KPI
    form_class = KPIForm
    template_name = "scorecards/kpis_create.html"


class EditScorecardKPI(ScorecardMixin, CoreUpdateView):
    model = KPI
    form_class = KPIForm
    template_name = "scorecards/kpis_edit.html"


class DeleteScorecardKPI(ScorecardMixin, CoreDeleteView):
    model = KPI
    template_name = "scorecards/kpis_delete.html"
