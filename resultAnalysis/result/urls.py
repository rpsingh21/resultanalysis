from django.conf.urls import url

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
	url(r'^$',getSessionAndsemester,name='home'),
	url(r'^addnewrollno/$',getNewResult,name='newResult'),
	url(r'^contact/$',contactUs,name='contact'),
	url(r'^report/error/$',reportError,name='reporterror'),
	url(r'^report/bug/$',reportBug,name='reportbug'),
	url(r'^results/(?P<college>[\w|\W]+)/(?P<branch>[\w|\W]+)/(?P<yearOfJoining>[\w|\W]+)/(?P<semester>[\w|\W]+)/(?P<subjectCode>[\w|\W]+)/$',showSubjectMarks,name='subjectMarks'),
	url(r'^results/(?P<college>[\w|\W]+)/(?P<branch>[\w|\W]+)/(?P<yearOfJoining>[\w|\W]+)/(?P<semester>[\w|\W]+)/$',showSemesterResult,name='semesterResult'),
	url(r'^result/(?P<rollNo>\d+)/(?P<semester>\d+)/$',studentSemesterResult,name='studentSemesterResult'),
]
