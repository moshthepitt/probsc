from django.conf.urls import url

from .views import KPIListview, AddKPI, EditKPI
from .views import DeleteKPI

urlpatterns = [
    url(r'^add/$', AddKPI.as_view(), name='kpis_add'),
    url(r'^edit/(?P<pk>\d+)/$', EditKPI.as_view(), name='kpis_edit'),
    url(r'^delete/(?P<pk>\d+)/$', DeleteKPI.as_view(), name='kpis_delete'),
    url(r'^list/$', KPIListview.as_view(), name='kpis_list'),
]
