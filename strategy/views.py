from django.views.generic.list import ListView

from braces.views import LoginRequiredMixin
from django_tables2 import SingleTableView

from .tables import StrategicThemeTable
from .models import StrategicTheme


class StrategicThemeListview(LoginRequiredMixin, SingleTableView, ListView):
    model = StrategicTheme
    table_class = StrategicThemeTable
    template_name = "strategy/strategic_theme_list.html"
    paginate_by = 25
