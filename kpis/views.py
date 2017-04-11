from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from scorecards.models import Scorecard
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


class ScorecardKPIListview(KPIListview):
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
        context['scorecard'] = self.scorecard
        context['create_view_url'] = reverse_lazy('kpis:kpis_add')
        context['list_view_url'] = reverse_lazy('scorecards:scorecards_kpis_list', args=[self.scorecard.pk])
        return context

    def dispatch(self, request, *args, **kwargs):
        self.scorecard = get_object_or_404(Scorecard, pk=kwargs.pop('pk', None))
        return super(ScorecardKPIListview, self).dispatch(request, *args, **kwargs)


class AddKPI(CoreCreateView):
    model = KPI
    form_class = KPIForm


class EditKPI(CoreUpdateView):
    model = KPI
    form_class = KPIForm


class DeleteKPI(CoreDeleteView):
    model = KPI
    success_url = reverse_lazy('kpis:kpis_list')
