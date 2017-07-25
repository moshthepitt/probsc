from datetime import datetime

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from .tables import ScorecardTable, UserScorecardTable, StaffScorecardTable
from .forms import ScorecardForm
from .models import Scorecard


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


class ScorecardListview(CoreListView):
    """ generic (admin) list of scorecards"""
    model = Scorecard
    table_class = ScorecardTable

    def get_context_data(self, **kwargs):
        context = super(ScorecardListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('scorecards:scorecards_add')
        context['list_view_url'] = reverse_lazy('scorecards:scorecards_list')
        return context


class StaffScorecards(CoreListView):
    """ manager/supervisor viewing his people's scorecards"""
    model = Scorecard
    table_class = StaffScorecardTable
    template_name = "scorecards/staff_scorecards.html"

    def get_context_data(self, **kwargs):
        context = super(StaffScorecards, self).get_context_data(**kwargs)
        context['create_view_url'] = "#"
        context['list_view_url'] = reverse_lazy('scorecards:staff_scorecards', args=[self.object.pk])
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
