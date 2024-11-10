"""resultAnalysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import re_path, include
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(('resultAnalyser.api.urls',
            'api-analysis'), namespace='api-analysis')),
    re_path(r'^newapi/', include(('result.api.urls',
            'newapi-analysis'), namespace='newapi-analysis')),
    re_path(r'^analysis/', include(('resultAnalyser.urls',
            'analysis'), namespace='analysis')),
    re_path(r'^account/', include(('account.urls', 'account'), namespace='account')),
    re_path(r'^', include(('result.urls', 'result'), namespace='result')),
    re_path(r'^xlsx/', include(('xlsx.urls', 'xlsx'), namespace='xlsx')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
