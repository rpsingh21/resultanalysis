from django import forms
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
)
from result.models import (
	College,
	Branch,
	Course,
	TotalMarks,
	Subject,
	Student,
	Marks,
	)


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	# doing forms vaildstions
	def clean(self,*args,**kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user=authenticate(username=username,password=password)
			if not user:
				raise forms.ValidationError("User does not exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")
			if not user.is_active:
				raise forms.ValidationError("user is not active")
		return super(UserLoginForm,self).clean(*args,**kwargs)

class AccountActionForm(forms.Form):
	# VALUE FOR CHOISE FIELDS
	semester=[(str(i),str(i)) for i in range(1,9)]
	
	# FORMS FIELDS 
	yearOfJoining = forms.ChoiceField(choices=Student.objects.values_list('yearOfJoining','yearOfJoining').distinct().order_by('yearOfJoining'))
	semester = forms.ChoiceField(choices=semester,required=True)
	branch = forms.ChoiceField(choices=Branch.objects.values_list('branchCode','branchName').order_by('branchCode'))
