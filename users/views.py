from django.urls import reverse_lazy
from django.db.models import Q

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from core.mixins import EditorAccess

from .tables import DepartmentTable, PositionTable, UserProfileTable
from .tables import SubordinatesTable
from .forms import DepartmentForm, PositionForm, UserProfileForm
from .forms import AddUserProfileForm
from .models import Department, Position, UserProfile


class DepartmentListview(EditorAccess, CoreListView):
    model = Department
    table_class = DepartmentTable
    search_fields = ['name', 'description', 'parent__name']

    def get_context_data(self, **kwargs):
        context = super(DepartmentListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('users:departments_add')
        context['list_view_url'] = reverse_lazy('users:departments_list')
        return context


class AddDepartment(EditorAccess, CoreCreateView):
    model = Department
    form_class = DepartmentForm


class EditDepartment(EditorAccess, CoreUpdateView):
    model = Department
    form_class = DepartmentForm


class DeleteDepartment(EditorAccess, CoreDeleteView):
    model = Department
    success_url = reverse_lazy('users:departments_list')


class PositionListview(EditorAccess, CoreListView):
    model = Position
    table_class = PositionTable
    search_fields = ['name', 'description', 'department__name', 'parent__name']

    def get_context_data(self, **kwargs):
        context = super(PositionListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('users:positions_add')
        context['list_view_url'] = reverse_lazy('users:positions_list')
        return context


class AddPosition(EditorAccess, CoreCreateView):
    model = Position
    form_class = PositionForm


class EditPosition(EditorAccess, CoreUpdateView):
    model = Position
    form_class = PositionForm


class DeletePosition(EditorAccess, CoreDeleteView):
    model = Position
    success_url = reverse_lazy('users:positions_list')


class UserProfileListview(EditorAccess, CoreListView):
    model = UserProfile
    table_class = UserProfileTable
    search_fields = ['user__first_name', 'user__last_name', 'user__email']

    def get_context_data(self, **kwargs):
        context = super(UserProfileListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('users:userprofiles_add')
        context['list_view_url'] = reverse_lazy('users:userprofiles_list')
        return context


class SubordinatesListview(CoreListView):
    table_class = SubordinatesTable
    model = UserProfile
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    template_name = "users/subordinates_list.html"

    def get_context_data(self, **kwargs):
        context = super(SubordinatesListview, self).get_context_data(**kwargs)
        context['create_view_url'] = "#"
        context['list_view_url'] = reverse_lazy('users:my_staff_list')
        return context

    def get_queryset(self):
        queryset = self.request.user.userprofile.get_subordinates()
        form = self.form_class(self.request.GET)
        if form.is_valid() and self.search_fields:
            search_terms = [
                "{}__icontains".format(x) for x in self.search_fields]
            query = Q()
            for term in search_terms:
                query.add(Q(**{term: form.cleaned_data['q']}), Q.OR)
            queryset = queryset.filter(query)
        return queryset


class AddUserProfile(EditorAccess, CoreCreateView):
    model = UserProfile
    form_class = AddUserProfileForm


class EditUserProfile(EditorAccess, CoreUpdateView):
    model = UserProfile
    form_class = UserProfileForm

    def get_initial(self):
        initial = super(EditUserProfile, self).get_initial()
        initial['first_name'] = self.object.user.first_name
        initial['last_name'] = self.object.user.last_name
        initial['email'] = self.object.user.email
        return initial
