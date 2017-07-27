from django import forms
from .models import (
	College,
	Branch,
	Course,
	TotalMarks,
	Subject,
	Student,
	Marks,
	)

class UrlForm(forms.Form):
	url = forms.URLField(widget=forms.URLInput(attrs={'class':'validate','id':'url'}))

	# DOING FROMS VAILDATIONS
	def clean_url(self,*args,**kwargs):
		url=self.cleaned_data.get('url')
		if not url[0:40]=='https://erp.aktu.ac.in/WebPages/OneView/':
			raise forms.ValidationError("INVALID URL!! Please enter a valid URL")
		return url

class SessionForm(forms.Form):
	# VALUE FOR CHOISE FIELDS
	semester=[(str(i),str(i)) for i in range(1,9)]

	# FORMS FIELDS 
	yearOfJoining = forms.ChoiceField(choices=Student.objects.values_list('yearOfJoining','yearOfJoining').distinct().order_by('yearOfJoining'))
	semester = forms.ChoiceField(choices=semester,required=True)
	college = forms.ModelChoiceField(queryset=College.objects.all().order_by('collegeCode'),empty_label="Select College")
	branch = forms.ModelChoiceField(queryset=Branch.objects.all().order_by('branchCode'),empty_label="select Branch")

## ORDERING FORM FOR RESULT
class OrderForm(forms.Form):
	choices=(
		('student__rollNo','Student Name'),
		('-internal','Internal Marks'),
		('-external','External Marks'),
		('-totalMarks','Total Marks')
		)
	order_by = forms.ChoiceField(choices=choices,required=False)

