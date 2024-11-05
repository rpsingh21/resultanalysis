from django.urls import re_path

from .views import (
	semseterResultxlsx,
	)

urlpatterns=[
	re_path(r'^semester-xlsx/(?P<collegeCode>\d+)/(?P<branchCode>\d+)/(?P<yearOfJoining>\d+)/(?P<semester>\d+)/$',semseterResultxlsx,name='semseterResultxlsx')
]
