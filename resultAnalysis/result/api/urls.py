from django.urls import re_path
from .views import (
	ContactUsCreateAPIView,
	ReportErrorCreateAPIView,
	ReportBugCreateAPIView,
	)

urlpatterns = [
    re_path(r'^contact/$',ContactUsCreateAPIView.as_view(),name="contact"),
    re_path(r'^reportbug/$',ReportErrorCreateAPIView.as_view(),name="reportBug"),
    re_path(r'^reporterror/$',ReportBugCreateAPIView.as_view(),name="reportError"),
]
  