from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from core.mixins import CoreFormMixin
from scorecards.models import Scorecard, ScorecardKPI
from scorecards.filters import ScorecardFilter
from scorecards.forms import ScorecardListViewSearchForm


class ScorecardKPIModalFormMixin(CoreFormMixin):

    """
    Common things for ScorecardKPI forms in modals
    """

    def get_initial(self):
        initial = super(ScorecardKPIModalFormMixin, self).get_initial()
        initial['scorecard'] = self.object.scorecard
        initial['kpi'] = self.object.kpi
        return initial

    def get_form_kwargs(self):
        kwargs = super(ScorecardKPIModalFormMixin, self).get_form_kwargs()
        kwargs['scorecard_kpi'] = self.object
        return kwargs


class ScorecardBelongsToUserMixin(object):

    """
    Used for objects with a scorecard field
    Ensures the scorecard belongs to the current user
    """

    def dispatch(self, *args, **kwargs):
        if self.get_object().scorecard.user != self.request.user:
            raise Http404
        return super(ScorecardBelongsToUserMixin, self).dispatch(
            *args, **kwargs)


class AccessScorecard(object):

    """
    Used for scorecard objects or objects with a scorecard field
    or with "self.scorecard"
    Ensures the scorecard belongs to the current user
    Or is being viewed by a supervisor or admin
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        subordinates = self.request.user.userprofile.get_subordinates()
        can_access = False
        if self.request.user.userprofile.can_edit():
            can_access = True
        elif (hasattr(self.get_object(), 'user')) and\
             (self.get_object().user.userprofile in subordinates):
            can_access = True
        else:
            if isinstance(self.get_object(), Scorecard):
                if self.get_object().user == self.request.user:
                    can_access = True
            else:
                if (hasattr(self.get_object(), 'scorecard')) and\
                   (self.get_object().scorecard.user == self.request.user):
                    can_access = True
        if not can_access:
            raise Http404
        return super(AccessScorecard, self).dispatch(*args, **kwargs)


class ScorecardMixin(object):

    """
    Adds scorecard to context
    """

    def get_context_data(self, **kwargs):
        context = super(ScorecardMixin, self).get_context_data(**kwargs)
        context['scorecard'] = self.scorecard
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.scorecard = get_object_or_404(
            Scorecard,
            pk=kwargs.pop('scorecard_pk', None))
        subordinates = self.request.user.userprofile.get_subordinates()
        can_access = False
        if (self.request.user.userprofile.can_edit()) or\
           (self.scorecard.user.userprofile in subordinates):
            can_access = True
        elif self.scorecard.user == self.request.user:
                can_access = True
        if not can_access:
            raise Http404
        return super(ScorecardMixin, self).dispatch(request, *args, **kwargs)


class ScorecardFormMixin(object):

    """
    Adds stuff for forms that have scorecard elements
    """

    def get_form_kwargs(self):
        kwargs = super(ScorecardFormMixin, self).get_form_kwargs()
        kwargs['scorecard'] = self.scorecard
        return kwargs


class KPICreateMixin(object):

    """
    Adds KPI that was created to scorecard
    """

    def get_form_kwargs(self):
        kwargs = super(ScorecardFormMixin, self).get_form_kwargs()
        kwargs['scorecard'] = self.scorecard
        return kwargs

    def form_valid(self, form):
        redirect_url = super(ScorecardFormMixin, self).form_valid(form)
        ScorecardKPI.objects.create(kpi=self.object, scorecard=self.scorecard)
        return redirect_url


class ScorecardQuersetMixin(object):
    """
    Process the queryset returned on scorecard list views
    """

    def get_queryset(self):
        queryset = super(ScorecardQuersetMixin, self).get_queryset()
        queryset = queryset.filter(user__userprofile__active=True)
        return queryset.distinct()


class ScorecardSearchMixin(object):
    """
    makes scorecard search better
    """
    filter_class = ScorecardFilter
    form_class = ScorecardListViewSearchForm
    search_fields = ['name', 'description', 'user__first_name',
                     'user__last_name', 'user__email']
    template_name = "scorecards/list.html"

    def get_context_data(self, **kwargs):
        context = super(ScorecardSearchMixin, self).get_context_data(
            **kwargs)
        initial = {'year': timezone.now().year}
        if self.request.GET.get('q'):
            initial['q'] = self.request.GET.get('q')
        if self.request.GET.get('year'):
            initial['year'] = self.request.GET.get('year')
        if self.request.GET.get('approved'):
            initial['approved'] = self.request.GET.get('approved')
        if self.request.GET.get('user__userprofile__position__department'):
            initial['user__userprofile__position__department'] = \
                self.request.GET.get('user__userprofile__position__department')
        form = self.form_class(request=self.request, initial=initial)
        context['form'] = form
        return context
