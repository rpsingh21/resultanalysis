from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
)

from .forms import (
	UserLoginForm,
	AccountActionForm,
	)

# Create your views here.
def login_view(request):
	form=UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user=authenticate(username=username, password=password)
		login(request, user)
		return HttpResponseRedirect(reverse('account:account'))
	content= {
	'title':'Login',
	'form':form,
	}
	return render(request,'account/login.html',content)

def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")

def account_view(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('account:login'))
	form = AccountActionForm(request.POST or None)
	if form.is_valid():
		yearOfJoining=form.cleaned_data.get('yearOfJoining')
		branch=form.cleaned_data.get('branch')
		semester=form.cleaned_data.get('semester')
		url_r=reverse('xlsx:semseterResultxlsx', kwargs={'collegeCode':187,'yearOfJoining':yearOfJoining,'branchCode':branch,'semester':semester})
		return HttpResponseRedirect(url_r)
	content={
	'title':'Report Download',
	'form':form,
	}
	return render(request,'account/userAction.html',content)

