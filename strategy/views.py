from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.translation import ugettext as _

from braces.views import LoginRequiredMixin, FormMessagesMixin
from django_tables2 import SingleTableView

from core.mixins import CoreFormMixin, ListViewSearchMixin, VerboseNameMixin
from customers.mixins import CustomerFormMixin
from .tables import StrategicThemeTable
from .forms import StrategicThemeForm
from .models import StrategicTheme


class StrategicThemeListview(LoginRequiredMixin, VerboseNameMixin, ListViewSearchMixin, SingleTableView, ListView):
    model = StrategicTheme
    table_class = StrategicThemeTable
    template_name = "core/crud/list.html"


class AddStrategicTheme(LoginRequiredMixin, FormMessagesMixin, VerboseNameMixin, CoreFormMixin, CustomerFormMixin, CreateView):
    model = StrategicTheme
    template_name = "core/crud/create.html"
    form_class = StrategicThemeForm
    form_valid_message = _("Saved successfully!")
    form_invalid_message = _("Please correct the errors below.")


class EditStrategicTheme(LoginRequiredMixin, FormMessagesMixin, VerboseNameMixin, CoreFormMixin, UpdateView):
    model = StrategicTheme
    form_class = StrategicThemeForm
    template_name = "core/crud/edit.html"
    form_valid_message = _("Saved successfully!")
    form_invalid_message = _("Please correct the errors below.")
