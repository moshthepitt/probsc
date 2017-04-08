from core.generic_views import CoreListView, CoreCreateView, CoreUpdateView
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
