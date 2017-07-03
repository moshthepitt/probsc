from django.conf.urls import url

from .views import DepartmentListview, AddDepartment, EditDepartment
from .views import DeleteDepartment

urlpatterns = [
    url(r'^departments/add/$', AddDepartment.as_view(), name='departments_add'),
    url(r'^departments/edit/(?P<pk>\d+)/$', EditDepartment.as_view(), name='departments_edit'),
    url(r'^departments/delete/(?P<pk>\d+)/$', DeleteDepartment.as_view(), name='departments_delete'),
    url(r'^departments/$', DepartmentListview.as_view(), name='departments_list'),
]
