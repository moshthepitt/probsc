from django.urls import reverse_lazy

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from .tables import StrategicThemeTable
from .forms import StrategicThemeForm
from .models import StrategicTheme


class StrategicThemeListview(CoreListView):
    model = StrategicTheme
    table_class = StrategicThemeTable


class AddStrategicTheme(CoreCreateView):
    model = StrategicTheme
    form_class = StrategicThemeForm


class EditStrategicTheme(CoreUpdateView):
    model = StrategicTheme
    form_class = StrategicThemeForm


class DeleteStrategicTheme(CoreDeleteView):
    model = StrategicTheme
    success_url = reverse_lazy('strategy:strategic_themes_list')
