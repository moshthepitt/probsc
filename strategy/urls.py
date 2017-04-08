from django.conf.urls import url

from .views import StrategicThemeListview, AddStrategicTheme, EditStrategicTheme
from .views import DeleteStrategicTheme, ObjectiveListview, AddObjective, EditObjective
from .views import DeleteObjective

urlpatterns = [
    url(r'^strategic-themes/add/$', AddStrategicTheme.as_view(), name='strategic_themes_add'),
    url(r'^strategic-themes/edit/(?P<pk>\d+)/$', EditStrategicTheme.as_view(), name='strategic_themes_edit'),
    url(r'^strategic-themes/delete/(?P<pk>\d+)/$', DeleteStrategicTheme.as_view(), name='strategic_themes_delete'),
    url(r'^strategic-themes/$', StrategicThemeListview.as_view(), name='strategic_themes_list'),
    url(r'^objectives/add/$', AddObjective.as_view(), name='objectives_add'),
    url(r'^objectives/edit/(?P<pk>\d+)/$', EditObjective.as_view(), name='objectives_edit'),
    url(r'^objectives/delete/(?P<pk>\d+)/$', DeleteObjective.as_view(), name='objectives_delete'),
    url(r'^objectives/$', ObjectiveListview.as_view(), name='objectives_list'),
]
