from django.conf.urls import url

from .views import StrategicThemeListview

urlpatterns = [
    url(r'^strategic-themes/$', StrategicThemeListview.as_view(), name='strategic_themes_list'),
]
