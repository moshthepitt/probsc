from django.urls import reverse_lazy

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from .tables import ScorecardTable
from .forms import ScorecardForm
from .models import Scorecard


class ScorecardListview(CoreListView):
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


class EditScorecard(CoreUpdateView):
    model = Scorecard
    form_class = ScorecardForm


class DeleteScorecard(CoreDeleteView):
    model = Scorecard
    success_url = reverse_lazy('scorecards:scorecards_list')
