from django.urls import reverse_lazy

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView

from .tables import DepartmentTable, PositionTable, UserProfileTable
from .tables import SubordinatesTable
from .forms import DepartmentForm, PositionForm, UserProfileForm
from .forms import AddUserProfileForm
from .models import Department, Position, UserProfile


class DepartmentListview(CoreListView):
    model = Department
    table_class = DepartmentTable
    search_fields = ['name', 'description', 'parent__name']

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


class PositionListview(CoreListView):
    model = Position
    table_class = PositionTable
    search_fields = ['name', 'description', 'department__name', 'parent__name']

    def get_context_data(self, **kwargs):
        context = super(PositionListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('users:positions_add')
        context['list_view_url'] = reverse_lazy('users:positions_list')
        return context


class AddPosition(CoreCreateView):
    model = Position
    form_class = PositionForm


class EditPosition(CoreUpdateView):
    model = Position
    form_class = PositionForm


class DeletePosition(CoreDeleteView):
    model = Position
    success_url = reverse_lazy('users:positions_list')


class UserProfileListview(CoreListView):
    model = UserProfile
    table_class = UserProfileTable
    search_fields = ['user__first_name', 'user__last_name', 'user__email']

    def get_context_data(self, **kwargs):
        context = super(UserProfileListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('users:userprofiles_add')
        context['list_view_url'] = reverse_lazy('users:userprofiles_list')
        return context


class SubordinatesListview(UserProfileListview):
    table_class = SubordinatesTable

    def get_queryset(self):
        return self.request.user.userprofile.get_subordinates()


class AddUserProfile(CoreCreateView):
    model = UserProfile
    form_class = AddUserProfileForm


class EditUserProfile(CoreUpdateView):
    model = UserProfile
    form_class = UserProfileForm

    def get_initial(self):
        initial = super(EditUserProfile, self).get_initial()
        initial['first_name'] = self.object.user.first_name
        initial['last_name'] = self.object.user.last_name
        initial['email'] = self.object.user.email
        return initial
