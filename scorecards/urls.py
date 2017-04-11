from django.conf.urls import url

from .views import ScorecardListview, AddScorecard, EditScorecard
from .views import DeleteScorecard

urlpatterns = [
    url(r'^add/$', AddScorecard.as_view(), name='scorecards_add'),
    url(r'^edit/(?P<pk>\d+)/$', EditScorecard.as_view(), name='scorecards_edit'),
    url(r'^delete/(?P<pk>\d+)/$', DeleteScorecard.as_view(), name='scorecards_delete'),
    url(r'^list/$', ScorecardListview.as_view(), name='scorecards_list'),
]
