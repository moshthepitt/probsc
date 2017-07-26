from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import ScorecardListview, AddScorecard, EditScorecard
from .views import DeleteScorecard, UserScorecards, StaffScorecards
from .views import UserScorecard, AddInitiativeSnippet, AddScoreSnippet
from .views import InitiativeListSnippet
from kpis.views import ScorecardKPIListview, AddScorecardKPI
from kpis.views import EditScorecardKPI, DeleteScorecardKPI
from .ajax import process_initiative_form

urlpatterns = [
    # ajax
    url(r'^ajax/add-initiative/$', login_required(process_initiative_form), name='process_initiative_form'),
    # scorecards
    url(r'^add/$', AddScorecard.as_view(), name='scorecards_add'),
    url(r'^edit/(?P<pk>\d+)/$', EditScorecard.as_view(), name='scorecards_edit'),
    url(r'^delete/(?P<pk>\d+)/$', DeleteScorecard.as_view(), name='scorecards_delete'),
    url(r'^staff-scorecards/(?P<pk>\d+)/$', StaffScorecards.as_view(), name='staff_scorecards'),
    url(r'^my-scorecard/(?P<pk>\d+)/$', UserScorecard.as_view(), name='user_scorecard'),
    url(r'^my-scorecards/$', UserScorecards.as_view(), name='user_scorecards'),
    url(r'^list/$', ScorecardListview.as_view(), name='scorecards_list'),
    # kpis
    url(r'^kpis/add/(?P<scorecard_pk>\d+)/$',
        AddScorecardKPI.as_view(), name='scorecards_kpis_add'),
    url(r'^kpis/edit/(?P<pk>\d+)/(?P<scorecard_pk>\d+)/$',
        EditScorecardKPI.as_view(), name='scorecards_kpis_edit'),
    url(r'^kpis/delete/(?P<pk>\d+)/(?P<scorecard_pk>\d+)/$',
        DeleteScorecardKPI.as_view(), name='scorecards_kpis_delete'),
    url(r'^kpis/(?P<scorecard_pk>\d+)/$',
        ScorecardKPIListview.as_view(), name='scorecards_kpis_list'),
    # snippets
    url(r'^snippets/add-initiative/(?P<pk>\d+)/$', AddInitiativeSnippet.as_view(),
        name='snippet_add_initiative'),
    url(r'^snippets/list-initiatives/(?P<pk>\d+)/$', InitiativeListSnippet.as_view(),
        name='snippet_list_initiatives'),
    url(r'^snippets/add-score/(?P<pk>\d+)/$', AddScoreSnippet.as_view(), name='snippet_add_score'),
]
