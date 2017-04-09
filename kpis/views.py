from django.urls import reverse_lazy

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from .tables import KPITable
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


class AddKPI(CoreCreateView):
    model = KPI
    form_class = KPIForm


class EditKPI(CoreUpdateView):
    model = KPI
    form_class = KPIForm


class DeleteKPI(CoreDeleteView):
    model = KPI
    success_url = reverse_lazy('kpis:kpis_list')
