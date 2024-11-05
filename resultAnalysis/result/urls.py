from django.urls import re_path

from .views import (
	getNewResult,
	getSessionAndsemester,
	showSemesterResult,
	showSubjectMarks,
	studentSemesterResult,
	contactUs,
	reportError,
	reportBug,
	)

urlpatterns=[
	re_path(r'^$',getSessionAndsemester,name='home'),
	re_path(r'^addnewrollno/$',getNewResult,name='newResult'),
	re_path(r'^contact/$',contactUs,name='contact'),
	re_path(r'^report/error/$',reportError,name='reporterror'),
	re_path(r'^report/bug/$',reportBug,name='reportbug'),
	re_path(r'^results/(?P<college>[\w|\W]+)/(?P<branch>[\w|\W]+)/(?P<yearOfJoining>[\w|\W]+)/(?P<semester>[\w|\W]+)/(?P<subjectCode>[\w|\W]+)/$',showSubjectMarks,name='subjectMarks'),
	re_path(r'^results/(?P<college>[\w|\W]+)/(?P<branch>[\w|\W]+)/(?P<yearOfJoining>[\w|\W]+)/(?P<semester>[\w|\W]+)/$',showSemesterResult,name='semesterResult'),
	re_path(r'^result/(?P<rollNo>\d+)/(?P<semester>\d+)/$',studentSemesterResult,name='studentSemesterResult'),
]
