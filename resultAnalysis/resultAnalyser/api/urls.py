from django.conf.urls import url

from . import views 

urlpatterns = [
	url(r'^(?P<rollNo>\d+)/(?P<semester>\d+)/$',views.StudentSemesterResultAPIView.as_view(),name='studentResultAPIView'),
	url(r'^(?P<rollNo>\d+)/$',views.StudentResultAPIView.as_view(),name='StudentResultAPIView'),
]