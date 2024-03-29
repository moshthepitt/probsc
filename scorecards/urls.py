from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import ScorecardListview, AddScorecard, EditScorecard
from .views import DeleteScorecard, UserScorecards, StaffScorecards
from .views import UserScorecard, AddInitiativeSnippet, AddScoreSnippet
from .views import InitiativeListSnippet, ScorecardReport, ScoreListSnippet
from .views import ScorecardReportsListview, UserAddScorecard, ApproveScorecard
from .views import StaffApproveScorecard, ScorecardEvidenceListview
from .views import EditScorecardEvidence, DeleteScorecardEvidence
from .views import AddScorecardEvidence
from .views import UserEditScorecard, UserDeleteScorecard, ScoreGraphSnippet
from kpis.views import ScorecardKPIListview, AddScorecardKPI
from kpis.views import EditScorecardKPI, DeleteScorecardKPI
from kpis.views import UserScorecardKPIListview, UserAddScorecardKPI
from kpis.views import UserEditScorecardKPI, UserDeleteScorecardKPI
from .ajax import process_initiative_form, process_score_form
from .ajax import delete_initiative, delete_score

urlpatterns = [
    # ajax
    url(r'^ajax/add-initiative/$', login_required(process_initiative_form),
        name='process_initiative_form'),
    url(r'^ajax/delete-initiative/(?P<pk>\d+)/$',
        login_required(delete_initiative), name='delete_initiative'),
    url(r'^ajax/add-score/$',
        login_required(process_score_form), name='process_score_form'),
    url(r'^ajax/delete-score/(?P<pk>\d+)/$',
        login_required(delete_score), name='delete_score'),
    # scorecards
    url(r'^add/$', AddScorecard.as_view(), name='scorecards_add'),
    url(r'^edit/(?P<pk>\d+)/$',
        EditScorecard.as_view(), name='scorecards_edit'),
    url(r'^approve/(?P<pk>\d+)/$',
        ApproveScorecard.as_view(), name='scorecards_approve'),
    url(r'^delete/(?P<pk>\d+)/$',
        DeleteScorecard.as_view(), name='scorecards_delete'),
    url(r'^staff-scorecards/(?P<pk>\d+)/$',
        StaffScorecards.as_view(), name='staff_scorecards'),
    url(r'^staff-scorecards/approve/(?P<pk>\d+)/$',
        StaffApproveScorecard.as_view(), name='staff_scorecards_approve'),
    url(r'^my-scorecards/add/$',
        UserAddScorecard.as_view(), name='user_scorecards_add'),
    url(r'^my-scorecards/edit/(?P<pk>\d+)/$',
        UserEditScorecard.as_view(), name='user_scorecards_edit'),
    url(r'^my-scorecards/delete/(?P<pk>\d+)/$',
        UserDeleteScorecard.as_view(), name='user_scorecards_delete'),
    url(r'^my-scorecards/$', UserScorecards.as_view(), name='user_scorecards'),
    url(r'^my-scorecard/(?P<pk>\d+)/$',
        UserScorecard.as_view(), name='user_scorecard'),
    url(r'^report/(?P<pk>\d+)/$',
        ScorecardReport.as_view(), name='scorecard_report'),
    url(r'^reports/$',
        ScorecardReportsListview.as_view(), name='scorecards_reports'),
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
    url(r'^my-kpis/add/(?P<scorecard_pk>\d+)/$',
        UserAddScorecardKPI.as_view(), name='user_scorecards_kpis_add'),
    url(r'^my-kpis/edit/(?P<pk>\d+)/(?P<scorecard_pk>\d+)/$',
        UserEditScorecardKPI.as_view(), name='user_scorecards_kpis_edit'),
    url(r'^my-kpis/delete/(?P<pk>\d+)/(?P<scorecard_pk>\d+)/$',
        UserDeleteScorecardKPI.as_view(), name='user_scorecards_kpis_delete'),
    url(r'^my-kpis/(?P<scorecard_pk>\d+)/$',
        UserScorecardKPIListview.as_view(), name='user_scorecards_kpis_list'),
    # evidence
    url(r'^evidence/add/(?P<scorecard_pk>\d+)/$',
        AddScorecardEvidence.as_view(), name='scorecard_evidence_add'),
    url(r'^evidence/edit/(?P<pk>\d+)/(?P<scorecard_pk>\d+)/$',
        EditScorecardEvidence.as_view(), name='scorecard_evidence_edit'),
    url(r'^evidence/delete/(?P<pk>\d+)/(?P<scorecard_pk>\d+)/$',
        DeleteScorecardEvidence.as_view(), name='scorecard_evidence_delete'),
    url(r'^evidence/(?P<scorecard_pk>\d+)/$',
        ScorecardEvidenceListview.as_view(), name='scorecard_evidence_list'),
    # snippets
    url(r'^snippets/add-initiative/(?P<pk>\d+)/$',
        AddInitiativeSnippet.as_view(),
        name='snippet_add_initiative'),
    url(r'^snippets/list-initiatives/(?P<pk>\d+)/$',
        InitiativeListSnippet.as_view(),
        name='snippet_list_initiatives'),
    url(r'^snippets/list-scores/(?P<pk>\d+)/$', ScoreListSnippet.as_view(),
        name='snippet_list_scores'),
    url(r'^snippets/graph-scores/(?P<pk>\d+)/$', ScoreGraphSnippet.as_view(),
        name='snippet_graph_scores'),
    url(r'^snippets/add-score/(?P<pk>\d+)/$',
        AddScoreSnippet.as_view(), name='snippet_add_score'),
]
