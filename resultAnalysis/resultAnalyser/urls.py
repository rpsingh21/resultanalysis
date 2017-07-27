from django.conf.urls import url

from .views import(
	studentResulAnalysis,
	compareResult,
	)

urlpatterns = [
	url(r'^student/(?P<rollNo>\d+)/$',studentResulAnalysis,name='studentResulAnalysis'),
	url(r'^student/$',studentResulAnalysis,name='studentResulAnalysisform'),
	url(r'^compare/$',compareResult,name="compare"),
]