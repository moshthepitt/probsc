from django.urls import reverse_lazy

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from core.mixins import EditorAccess
from .tables import StrategicThemeTable, ObjectiveTable
from .forms import StrategicThemeForm, ObjectiveForm
from .models import StrategicTheme, Objective


class StrategicThemeListview(EditorAccess, CoreListView):
    model = StrategicTheme
    table_class = StrategicThemeTable

    def get_context_data(self, **kwargs):
        context = super(StrategicThemeListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('strategy:strategic_themes_add')
        context['list_view_url'] = reverse_lazy('strategy:strategic_themes_list')
        return context


class AddStrategicTheme(EditorAccess, CoreCreateView):
    model = StrategicTheme
    form_class = StrategicThemeForm


class EditStrategicTheme(EditorAccess, CoreUpdateView):
    model = StrategicTheme
    form_class = StrategicThemeForm


class DeleteStrategicTheme(EditorAccess, CoreDeleteView):
    model = StrategicTheme
    success_url = reverse_lazy('strategy:strategic_themes_list')


class ObjectiveListview(EditorAccess, CoreListView):
    model = Objective
    table_class = ObjectiveTable

    def get_context_data(self, **kwargs):
        context = super(ObjectiveListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('strategy:objectives_add')
        context['list_view_url'] = reverse_lazy('strategy:objectives_list')
        return context


class AddObjective(EditorAccess, CoreCreateView):
    model = Objective
    form_class = ObjectiveForm


class EditObjective(EditorAccess, CoreUpdateView):
    model = Objective
    form_class = ObjectiveForm


class DeleteObjective(EditorAccess, CoreDeleteView):
    model = Objective
    success_url = reverse_lazy('strategy:objectives_list')
