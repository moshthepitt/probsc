from django.utils.translation import ugettext as _
from django.urls import reverse, reverse_lazy
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib import messages

from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from core.mixins import EditorAccess

from scorecards.mixins import ScorecardMixin, ScorecardFormMixin
from scorecards.mixins import KPICreateMixin
from .tables import KPITable, ScorecardKPITable, UserScorecardKPITable
from .forms import KPIForm, UserKPIForm
from .models import KPI


class KPIListview(EditorAccess, CoreListView):
    model = KPI
    table_class = KPITable
    search_fields = ['name', 'measure', 'description']

    def get_context_data(self, **kwargs):
        context = super(KPIListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('kpis:kpis_add')
        context['list_view_url'] = reverse_lazy('kpis:kpis_list')
        return context


class ScorecardKPIListview(ScorecardMixin, KPIListview):
    template_name = "scorecards/kpis_list.html"
    table_class = ScorecardKPITable

    def get_table_kwargs(self):
        kwargs = super(ScorecardKPIListview, self).get_table_kwargs()
        kwargs['scorecard'] = self.scorecard
        return kwargs

    def get_queryset(self):
        queryset = super(ScorecardKPIListview, self).get_queryset()
        return queryset.filter(scorecard=self.scorecard)

    def get_context_data(self, **kwargs):
        context = super(ScorecardKPIListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy(
            'scorecards:scorecards_kpis_add', args=[self.scorecard.pk])
        context['list_view_url'] = reverse_lazy(
            'scorecards:scorecards_kpis_list', args=[self.scorecard.pk])
        return context


class AddKPI(EditorAccess, CoreCreateView):
    model = KPI
    form_class = KPIForm


class EditKPI(EditorAccess, CoreUpdateView):
    model = KPI
    form_class = KPIForm


class DeleteKPI(EditorAccess, CoreDeleteView):
    model = KPI
    success_url = reverse_lazy('kpis:kpis_list')


class AddScorecardKPI(KPICreateMixin, ScorecardFormMixin, ScorecardMixin, CoreCreateView):
    model = KPI
    form_class = KPIForm
    template_name = "scorecards/kpis_create.html"


class EditScorecardKPI(ScorecardFormMixin, ScorecardMixin, CoreUpdateView):
    model = KPI
    form_class = KPIForm
    template_name = "scorecards/kpis_edit.html"


class DeleteScorecardKPI(ScorecardMixin, CoreDeleteView):
    model = KPI
    template_name = "scorecards/kpis_delete.html"

    def get_success_url(self):
        return reverse('scorecards:scorecards_kpis_list', args=[self.scorecard.id])

    def delete(self, request, *args, **kwargs):
        try:
            return super(CoreDeleteView, self).delete(request, *args, **kwargs)
        except ProtectedError:
            info = _("You cannot delete this item, it is referenced by other items.")
            messages.error(request, info, fail_silently=True)
            return redirect(reverse('scorecards:scorecards_kpis_delete',
                                    args=[self.object.id, self.scorecard.id]))


class UserScorecardKPIListview(ScorecardKPIListview):
    template_name = "scorecards/kpis_list.html"
    table_class = UserScorecardKPITable

    def get_context_data(self, **kwargs):
        context = super(UserScorecardKPIListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy(
            'scorecards:user_scorecards_kpis_add', args=[self.scorecard.pk])
        context['list_view_url'] = reverse_lazy(
            'scorecards:user_scorecards_kpis_list', args=[self.scorecard.pk])
        return context


class UserAddScorecardKPI(AddScorecardKPI):
    form_class = UserKPIForm

    def get_success_url(self):
        return reverse('scorecards:user_scorecards_kpis_list', args=[self.scorecard.id])


class UserEditScorecardKPI(EditScorecardKPI):
    form_class = UserKPIForm

    def get_success_url(self):
        return reverse('scorecards:user_scorecards_kpis_list', args=[self.scorecard.id])


class UserDeleteScorecardKPI(ScorecardMixin, CoreDeleteView):
    model = KPI
    template_name = "scorecards/user_kpis_delete.html"

    def get_success_url(self):
        return reverse('scorecards:user_scorecards_kpis_list', args=[self.scorecard.id])

    def delete(self, request, *args, **kwargs):
        try:
            return super(CoreDeleteView, self).delete(request, *args, **kwargs)
        except ProtectedError:
            info = _("You cannot delete this item, it is referenced by other items.")
            messages.error(request, info, fail_silently=True)
            return redirect(reverse('scorecards:user_scorecards_kpis_delete',
                                    args=[self.object.id, self.scorecard.id]))
