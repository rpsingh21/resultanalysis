from django.conf.urls import url, include
from .views import (
	login_view,
	account_view,
	logout_view,
	)
urlpatterns = [
    url(r'^login/$',login_view,name="login"),
    url(r'^logout/$',logout_view,name='logout'),
    url(r'^$',account_view,name='account'),
    ]