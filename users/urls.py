from django.conf.urls import url

from .views import DepartmentListview, AddDepartment, EditDepartment
from .views import DeleteDepartment, PositionListview, AddPosition
from .views import EditPosition, DeletePosition

urlpatterns = [
    url(r'^departments/add/$', AddDepartment.as_view(), name='departments_add'),
    url(r'^departments/edit/(?P<pk>\d+)/$', EditDepartment.as_view(), name='departments_edit'),
    url(r'^departments/delete/(?P<pk>\d+)/$', DeleteDepartment.as_view(), name='departments_delete'),
    url(r'^departments/$', DepartmentListview.as_view(), name='departments_list'),
    url(r'^positions/add/$', AddPosition.as_view(), name='positions_add'),
    url(r'^positions/edit/(?P<pk>\d+)/$', EditPosition.as_view(), name='positions_edit'),
    url(r'^positions/delete/(?P<pk>\d+)/$', DeletePosition.as_view(), name='positions_delete'),
    url(r'^positions/$', PositionListview.as_view(), name='positions_list'),
]
