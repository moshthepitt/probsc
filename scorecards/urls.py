from django.conf.urls import url

from .views import ScorecardListview, AddScorecard, EditScorecard
from .views import DeleteScorecard
from kpis.views import ScorecardKPIListview

urlpatterns = [
    url(r'^add/$', AddScorecard.as_view(), name='scorecards_add'),
    url(r'^edit/(?P<pk>\d+)/$', EditScorecard.as_view(), name='scorecards_edit'),
    url(r'^delete/(?P<pk>\d+)/$', DeleteScorecard.as_view(), name='scorecards_delete'),
    url(r'^kpis/(?P<pk>\d+)/$', ScorecardKPIListview.as_view(), name='scorecards_kpis_list'),
    url(r'^list/$', ScorecardListview.as_view(), name='scorecards_list'),
]
