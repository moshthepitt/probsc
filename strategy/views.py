from django.urls import reverse_lazy

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from .tables import StrategicThemeTable, ObjectiveTable
from .forms import StrategicThemeForm, ObjectiveForm
from .models import StrategicTheme, Objective


class StrategicThemeListview(CoreListView):
    model = StrategicTheme
    table_class = StrategicThemeTable

    def get_context_data(self, **kwargs):
        context = super(StrategicThemeListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('strategy:strategic_themes_add')
        context['list_view_url'] = reverse_lazy('strategy:strategic_themes_list')
        return context


class AddStrategicTheme(CoreCreateView):
    model = StrategicTheme
    form_class = StrategicThemeForm


class EditStrategicTheme(CoreUpdateView):
    model = StrategicTheme
    form_class = StrategicThemeForm


class DeleteStrategicTheme(CoreDeleteView):
    model = StrategicTheme
    success_url = reverse_lazy('strategy:strategic_themes_list')


class ObjectiveListview(CoreListView):
    model = Objective
    table_class = ObjectiveTable

    def get_context_data(self, **kwargs):
        context = super(ObjectiveListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('strategy:objectives_add')
        context['list_view_url'] = reverse_lazy('strategy:objectives_list')
        return context


class AddObjective(CoreCreateView):
    model = Objective
    form_class = ObjectiveForm


class EditObjective(CoreUpdateView):
    model = Objective
    form_class = ObjectiveForm


class DeleteObjective(CoreDeleteView):
    model = Objective
    success_url = reverse_lazy('strategy:objectives_list')
