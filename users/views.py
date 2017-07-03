from django.urls import reverse_lazy

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView

from .tables import DepartmentTable
from .forms import DepartmentForm
from .models import Department


class DepartmentListview(CoreListView):
    model = Department
    table_class = DepartmentTable

    def get_context_data(self, **kwargs):
        context = super(DepartmentListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('users:departments_add')
        context['list_view_url'] = reverse_lazy('users:departments_list')
        return context


class AddDepartment(CoreCreateView):
    model = Department
    form_class = DepartmentForm


class EditDepartment(CoreUpdateView):
    model = Department
    form_class = DepartmentForm


class DeleteDepartment(CoreDeleteView):
    model = Department
    success_url = reverse_lazy('users:departments_list')
