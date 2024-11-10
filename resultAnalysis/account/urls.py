from django.urls import re_path
from .views import (
    login_view,
    account_view,
    logout_view,
)
urlpatterns = [
    re_path(r'^login/$', login_view, name="login"),
    re_path(r'^logout/$', logout_view, name='logout'),
    re_path(r'^$', account_view, name='account'),
]
