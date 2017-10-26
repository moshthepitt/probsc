from datetime import datetime

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.contrib import messages

from django_tables2 import SingleTableMixin
from braces.views import LoginRequiredMixin

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from core.generic_views import CoreGenericDeleteView
from core.mixins import VerboseNameMixin, EditorAccess
from users.mixins import BelongsToUserMixin
from scorecards.mixins import ScorecardMixin, ScorecardFormMixin
from .tables import ScorecardTable, UserScorecardTable, StaffScorecardTable
from .tables import UserScorecardKPITable, InitiativeTable, EvidenceTable
from .tables import ScorecardReportKPITable, ScorecardReportTable, ScoreTable
from .forms import ScorecardForm, InitiativeModalForm, ScoreModalForm
from .forms import UserScorecardForm, ScorecardApprovalForm
from .forms import StaffScorecardApprovalForm, EvidenceForm
from .mixins import ScorecardKPIModalFormMixin, AccessScorecard
from .models import Scorecard, ScorecardKPI, Initiative, Score, Evidence


class InitiativeListSnippet(LoginRequiredMixin, AccessScorecard,
                            SingleTableMixin, DetailView):
    model = ScorecardKPI
    table_class = InitiativeTable
    template_name = "scorecards/snippets/list_initiatives.html"

    def get_table_data(self):
        return Initiative.objects.filter(kpi=self.object.kpi,
                                         scorecard=self.object.scorecard)


class ScoreListSnippet(LoginRequiredMixin, AccessScorecard,
                       SingleTableMixin, DetailView):
    model = ScorecardKPI
    table_class = ScoreTable
    template_name = "scorecards/snippets/list_scores.html"

    def get_table_data(self):
        return Score.objects.filter(kpi=self.object.kpi,
                                    scorecard=self.object.scorecard)


class ScoreGraphSnippet(LoginRequiredMixin, AccessScorecard, DetailView):
    model = ScorecardKPI
    template_name = "scorecards/snippets/graph_scores.html"

    def get_table_data(self):
        return Score.objects.filter(kpi=self.object.kpi,
                                    scorecard=self.object.scorecard)

    def get_context_data(self, **kwargs):
        context = super(ScoreGraphSnippet, self).get_context_data(**kwargs)
        scores = Score.objects.filter(kpi=self.object.kpi,
                                      scorecard=self.object.scorecard)
        context['scores'] = scores
        return context


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
        return Score.objects.filter(kpi=self.object.kpi,
                                    scorecard=self.object.scorecard)


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


class ScorecardReportsListview(EditorAccess, CoreListView):

    """ generic (admin) list of scorecards"""
    model = Scorecard
    table_class = ScorecardReportTable
    template_name = "scorecards/reports.html"


class ScorecardListview(EditorAccess, CoreListView):

    """ generic (admin) list of scorecards"""
    model = Scorecard
    table_class = ScorecardTable

    def get_context_data(self, **kwargs):
        context = super(ScorecardListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('scorecards:scorecards_add')
        context['list_view_url'] = reverse_lazy('scorecards:scorecards_list')
        return context


class AddScorecard(EditorAccess, CoreCreateView):
    model = Scorecard
    form_class = ScorecardForm

    def get_initial(self):
        initial = super(AddScorecard, self).get_initial()
        initial['year'] = datetime.now().year
        return initial


class EditScorecard(EditorAccess, CoreUpdateView):
    model = Scorecard
    form_class = ScorecardForm


class ApproveScorecard(AccessScorecard, CoreUpdateView):
    model = Scorecard
    form_class = ScorecardApprovalForm
    template_name = "scorecards/approve.html"

    def get_initial(self):
        initial = super(ApproveScorecard, self).get_initial()
        initial['approved_by'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse('scorecards:scorecards_list')

    def dispatch(self, request, *args, **kwargs):
        # cannot approve your own scorecard
        if self.get_object().user == request.user:
            messages.error(request,
                           _("You cannot approve your own scorecard"),
                           fail_silently=True)
            return redirect(reverse('scorecards:user_scorecards'))
        return super(ApproveScorecard, self).dispatch(request, *args, **kwargs)


class StaffApproveScorecard(ApproveScorecard):
    form_class = StaffScorecardApprovalForm

    def get_success_url(self):
        return reverse('scorecards:staff_scorecards')


class DeleteScorecard(EditorAccess, CoreDeleteView):
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
        return reverse('scorecards:user_scorecards_edit',
                       args=[self.object.id])


class UserEditScorecard(CoreUpdateView):

    """ the user editting his own scorecard"""
    model = Scorecard
    form_class = UserScorecardForm

    def get_initial(self):
        initial = super(UserEditScorecard, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse('scorecards:user_scorecards_edit',
                       args=[self.object.id])


class UserDeleteScorecard(AccessScorecard, CoreGenericDeleteView):

    """ the user deleting his own scorecard """
    model = Scorecard
    template_name = "scorecards/user_scorecard_delete.html"

    def get_success_url(self):
        return reverse('scorecards:user_scorecards')

    def delete(self, request, *args, **kwargs):
        try:
            return super(UserDeleteScorecard, self).delete(request,
                                                           *args,
                                                           **kwargs)
        except ProtectedError:
            info = _("You cannot delete this item, it is referenced by other "
                     "items.")
            messages.error(request, info, fail_silently=True)
            return redirect(reverse('scorecards:user_scorecards_delete',
                                    args=[self.object.id]))


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


class ScorecardEvidenceListview(ScorecardMixin, CoreListView):
    model = Evidence
    table_class = EvidenceTable
    search_fields = ['name']

    def get_queryset(self):
        queryset = super(ScorecardEvidenceListview, self).get_queryset()
        return queryset.filter(scorecard=self.scorecard)

    def get_context_data(self, **kwargs):
        context = super(ScorecardEvidenceListview, self).get_context_data(
            **kwargs)
        context['create_view_url'] = reverse_lazy(
            'scorecards:scorecard_evidence_add', args=[self.scorecard.pk])
        context['list_view_url'] = reverse_lazy(
            'scorecards:scorecard_evidence_list', args=[self.scorecard.pk])
        return context


class AddScorecardEvidence(ScorecardFormMixin, ScorecardMixin,
                           CoreCreateView):
    model = Evidence
    form_class = EvidenceForm

    def get_initial(self):
        initial = super(AddScorecardEvidence, self).get_initial()
        initial['scorecard'] = self.scorecard
        return initial

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse('scorecards:scorecard_evidence_list',
                       args=[self.scorecard.pk])


class EditScorecardEvidence(ScorecardFormMixin, ScorecardMixin,
                            CoreUpdateView):
    model = Evidence
    form_class = EvidenceForm

    def get_success_url(self):
        return reverse('scorecards:scorecard_evidence_list',
                       args=[self.scorecard.pk])


class DeleteScorecardEvidence(ScorecardMixin, CoreDeleteView):
    model = Evidence

    def get_success_url(self):
        return reverse('scorecards:scorecard_evidence_list', args=[
            self.scorecard.id])
