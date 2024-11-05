from django.urls import re_path

from .views import(
	studentResulAnalysis,
	compareResult,
	)

urlpatterns = [
	re_path(r'^student/(?P<rollNo>\d+)/$',studentResulAnalysis,name='studentResulAnalysis'),
	re_path(r'^student/$',studentResulAnalysis,name='studentResulAnalysisform'),
	re_path(r'^compare/$',compareResult,name="compare"),
]