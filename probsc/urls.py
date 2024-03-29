"""probsc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from django.conf import settings

from core.views import HomePageView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^kpis/', include('kpis.urls', namespace='kpis')),
    url(r'^scorecards/', include('scorecards.urls', namespace='scorecards')),
    url(r'^staff/', include('users.urls', namespace='users')),
    url(r'^strategy/', include('strategy.urls', namespace='strategy')),

    # third party
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),

    # this should be last
    url(r'^page/', include('django.contrib.flatpages.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    # static files (images, css, javascript, etc.)
    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    ]
