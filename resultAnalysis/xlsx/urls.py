from django.conf.urls import url

from .views import (
	semseterResultxlsx,
	)

urlpatterns=[
	url(r'^semester-xlsx/(?P<collegeCode>\d+)/(?P<branchCode>\d+)/(?P<yearOfJoining>\d+)/(?P<semester>\d+)/$',semseterResultxlsx,name='semseterResultxlsx')
]
