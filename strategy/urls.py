from django.conf.urls import url

from .views import StrategicThemeListview, AddStrategicTheme, EditStrategicTheme

urlpatterns = [
    url(r'^strategic-themes/add/$', AddStrategicTheme.as_view(), name='strategic_themes_add'),
    url(r'^strategic-themes/edit/(?P<pk>\d+)/$', EditStrategicTheme.as_view(), name='strategic_themes_edit'),
    url(r'^strategic-themes/$', StrategicThemeListview.as_view(), name='strategic_themes_list'),
]
