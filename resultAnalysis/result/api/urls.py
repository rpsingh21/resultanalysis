from django.conf.urls import url
from .views import (
	ContactUsCreateAPIView,
	ReportErrorCreateAPIView,
	ReportBugCreateAPIView,
	)

urlpatterns = [
    url(r'^contact/$',ContactUsCreateAPIView.as_view(),name="contact"),
    url(r'^reportbug/$',ReportErrorCreateAPIView.as_view(),name="reportBug"),
    url(r'^reporterror/$',ReportBugCreateAPIView.as_view(),name="reportError"),
]
  