from django.conf.urls import url

from .views import ScorecardListview, AddScorecard, EditScorecard
from .views import DeleteScorecard
from kpis.views import ScorecardKPIListview, AddScorecardKPI
from kpis.views import EditScorecardKPI, DeleteScorecardKPI

urlpatterns = [
    url(r'^add/$', AddScorecard.as_view(), name='scorecards_add'),
    url(r'^edit/(?P<pk>\d+)/$', EditScorecard.as_view(), name='scorecards_edit'),
    url(r'^delete/(?P<pk>\d+)/$', DeleteScorecard.as_view(), name='scorecards_delete'),
    url(r'^kpis/add/(?P<scorecard_pk>\d+)/$',
        AddScorecardKPI.as_view(), name='scorecards_kpis_add'),
    url(r'^kpis/edit/(?P<pk>\d+)/(?P<scorecard_pk>\d+)/$',
        EditScorecardKPI.as_view(), name='scorecards_kpis_edit'),
    url(r'^kpis/delete/(?P<pk>\d+)/(?P<scorecard_pk>\d+)/$',
        DeleteScorecardKPI.as_view(), name='scorecards_kpis_delete'),
    url(r'^kpis/(?P<scorecard_pk>\d+)/$',
        ScorecardKPIListview.as_view(), name='scorecards_kpis_list'),
    url(r'^list/$', ScorecardListview.as_view(), name='scorecards_list'),
]
