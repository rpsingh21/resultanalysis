from django.urls import re_path

from . import views 

urlpatterns = [
	re_path(r'^(?P<rollNo>\d+)/(?P<semester>\d+)/$',views.StudentSemesterResultAPIView.as_view(),name='studentResultAPIView'),
	re_path(r'^(?P<rollNo>\d+)/$',views.StudentResultAPIView.as_view(),name='StudentResultAPIView'),
]