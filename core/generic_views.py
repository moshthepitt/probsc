from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.translation import ugettext as _

from braces.views import LoginRequiredMixin, FormMessagesMixin
from django_tables2 import SingleTableView

from core.mixins import CoreFormMixin, ListViewSearchMixin, VerboseNameMixin
from customers.mixins import CustomerFormMixin, CustomerCheckMixin, CustomerExistsMixin
from customers.mixins import CustomerFilterMixin


class CoreListView(LoginRequiredMixin, CustomerExistsMixin, CustomerFilterMixin, VerboseNameMixin, ListViewSearchMixin, SingleTableView, ListView):
    template_name = "core/crud/list.html"


class CoreCreateView(LoginRequiredMixin, CustomerExistsMixin, FormMessagesMixin, VerboseNameMixin, CoreFormMixin, CustomerFormMixin, CreateView):
    template_name = "core/crud/create.html"
    form_valid_message = _("Saved successfully!")
    form_invalid_message = _("Please correct the errors below.")


class CoreUpdateView(LoginRequiredMixin, CustomerCheckMixin, FormMessagesMixin, VerboseNameMixin, CoreFormMixin, UpdateView):
    template_name = "core/crud/edit.html"
    form_valid_message = _("Saved successfully!")
    form_invalid_message = _("Please correct the errors below.")
