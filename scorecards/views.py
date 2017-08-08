from datetime import datetime

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin

from django_tables2 import SingleTableMixin
from braces.views import LoginRequiredMixin

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from core.mixins import VerboseNameMixin
from users.mixins import BelongsToUserMixin
from .tables import ScorecardTable, UserScorecardTable, StaffScorecardTable
from .tables import UserScorecardKPITable, InitiativeTable, ScoreTable
from .tables import ScorecardReportKPITable, ScorecardReportTable
from .forms import ScorecardForm, InitiativeModalForm, ScoreModalForm
from .forms import UserScorecardForm
from .mixins import ScorecardKPIModalFormMixin, AccessScorecard
from .models import Scorecard, ScorecardKPI, Initiative, Score


class InitiativeListSnippet(LoginRequiredMixin, AccessScorecard, SingleTableMixin,
                            DetailView):
    model = ScorecardKPI
    table_class = InitiativeTable
    template_name = "scorecards/snippets/list_initiatives.html"

    def get_table_data(self):
        return Initiative.objects.filter(kpi=self.object.kpi, scorecard=self.object.scorecard)


class ScoreListSnippet(LoginRequiredMixin, AccessScorecard, SingleTableMixin, DetailView):
    model = ScorecardKPI
    table_class = ScoreTable
    template_name = "scorecards/snippets/list_scores.html"

    def get_table_data(self):
        return Score.objects.filter(kpi=self.object.kpi, scorecard=self.object.scorecard)


class AddInitiativeSnippet(LoginRequiredMixin, AccessScorecard,
                           ScorecardKPIModalFormMixin, FormMixin, DetailView):
    model = ScorecardKPI
    template_name = "scorecards/snippets/add_initiative.html"
    success_url = "#"
    form_class = InitiativeModalForm


class AddScoreSnippet(LoginRequiredMixin, AccessScorecard, SingleTableMixin,
                      ScorecardKPIModalFormMixin, FormMixin, DetailView):
    model = ScorecardKPI
    template_name = "scorecards/snippets/add_score.html"
    success_url = "#"
    form_class = ScoreModalForm
    table_class = ScoreTable

    def get_table_data(self):
        return Score.objects.filter(kpi=self.object.kpi, scorecard=self.object.scorecard)


class ScorecardReport(LoginRequiredMixin, AccessScorecard, VerboseNameMixin,
                      SingleTableMixin, DetailView):

    """the scorecard report """
    model = Scorecard
    table_class = ScorecardReportKPITable
    template_name = "scorecards/report.html"

    def get_kpis(self):
        kpis = self.object.get_report()['kpis']
        return kpis

    def get_table_data(self):
        return self.get_kpis()


class UserScorecard(LoginRequiredMixin, VerboseNameMixin, BelongsToUserMixin,
                    SingleTableMixin, DetailView):

    """the user viewing his/her own scorecard"""
    model = Scorecard
    table_class = UserScorecardKPITable
    template_name = "scorecards/user_scorecard.html"

    def get_kpis(self):
        kpis = self.object.get_report()['kpis']
        return kpis

    def get_table_data(self):
        return self.get_kpis()


class StaffScorecards(CoreListView):

    """ manager/supervisor viewing his people's scorecards"""
    model = Scorecard
    table_class = StaffScorecardTable
    template_name = "scorecards/staff_scorecards.html"

    def get_context_data(self, **kwargs):
        context = super(StaffScorecards, self).get_context_data(**kwargs)
        context['create_view_url'] = "#"
        context['list_view_url'] = reverse_lazy(
            'scorecards:staff_scorecards', args=[self.object.pk])
        context['this_object'] = self.object
        return context

    def get_queryset(self):
        queryset = super(StaffScorecards, self).get_queryset()
        queryset = queryset.filter(user=self.object)
        return queryset

    def dispatch(self, *args, **kwargs):
        self.object = get_object_or_404(User, pk=self.kwargs['pk'])
        # if this user is not a subordinate then 404 away
        subordinates = self.request.user.userprofile.get_subordinates()
        if self.object.userprofile not in subordinates:
            raise Http404
        return super(StaffScorecards, self).dispatch(*args, **kwargs)


class ScorecardReportsListview(CoreListView):

    """ generic (admin) list of scorecards"""
    model = Scorecard
    table_class = ScorecardReportTable
    template_name = "scorecards/reports.html"


class ScorecardListview(CoreListView):

    """ generic (admin) list of scorecards"""
    model = Scorecard
    table_class = ScorecardTable

    def get_context_data(self, **kwargs):
        context = super(ScorecardListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('scorecards:scorecards_add')
        context['list_view_url'] = reverse_lazy('scorecards:scorecards_list')
        return context


class AddScorecard(CoreCreateView):
    model = Scorecard
    form_class = ScorecardForm

    def get_initial(self):
        initial = super(AddScorecard, self).get_initial()
        initial['year'] = datetime.now().year
        return initial


class EditScorecard(CoreUpdateView):
    model = Scorecard
    form_class = ScorecardForm


class DeleteScorecard(CoreDeleteView):
    model = Scorecard
    success_url = reverse_lazy('scorecards:scorecards_list')


class UserAddScorecard(CoreCreateView):
    """ the user adding his own scorecard"""
    model = Scorecard
    form_class = UserScorecardForm

    def get_initial(self):
        initial = super(UserAddScorecard, self).get_initial()
        initial['year'] = datetime.now().year
        initial['user'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse('scorecards:user_scorecards_edit', args=[self.object.id])


class UserEditScorecard(AccessScorecard, EditScorecard):
    """ the user editting his own scorecard"""
    model = Scorecard
    form_class = UserScorecardForm

    def get_initial(self):
        initial = super(UserEditScorecard, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse('scorecards:user_scorecards_edit', args=[self.object.id])


class UserDeleteScorecard(AccessScorecard, DeleteScorecard):
    """ the user deleting his own scorecard """
    model = Scorecard
    success_url = reverse_lazy('scorecards:user_scorecards')


class UserScorecards(CoreListView):

    """the user viewing his own scorecards"""
    model = Scorecard
    table_class = UserScorecardTable
    template_name = "scorecards/user_scorecards.html"

    def get_context_data(self, **kwargs):
        context = super(UserScorecards, self).get_context_data(**kwargs)
        context['create_view_url'] = "#"
        context['list_view_url'] = reverse_lazy('scorecards:user_scorecards')
        context['this_object'] = self.object
        return context

    def get_queryset(self):
        queryset = super(UserScorecards, self).get_queryset()
        queryset = queryset.filter(user=self.object)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        self.object = request.user
        return super(UserScorecards, self).dispatch(request, *args, **kwargs)
