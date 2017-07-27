from django import forms
from result.models import Student

class CompareForm(forms.Form):
	baseStudent = forms.CharField(max_length=14,required=True)
	otherStudent = forms.CharField(max_length=14,required=True)
	def clean_baseStudent(self,*args,**kwargs):
		rollNo=self.cleaned_data.get('baseStudent').strip()
		studnetObj = Student.objects.filter(rollNo=rollNo)
		if studnetObj.exists():
			return rollNo
		raise forms.ValidationError("Roll No. does not exists")

	def clean_otherStudent(self,*args,**kwargs):
		rollNo=self.cleaned_data.get('otherStudent').strip()
		studnetObj = Student.objects.filter(rollNo=rollNo)
		if studnetObj.exists():
			return rollNo
		raise forms.ValidationError("Roll No. does not exists")

	def clean(self):
		cleaned_data = super(CompareForm, self).clean()
		rollNo1 = cleaned_data.get('baseStudent')
		rollNo2 = cleaned_data.get('otherStudent')
		if rollNo1 and rollNo2:
			if rollNo1 == rollNo2:
				raise forms.ValidationError("Roll numbers should be distinct")


