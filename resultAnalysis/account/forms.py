from django import forms
from django.contrib.auth import (
    authenticate,
)
from result.models import (
    Branch,
    Student,
)


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # doing forms vaildstions
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("User does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("user is not active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class AccountActionForm(forms.Form):
    # VALUE FOR CHOISE FIELDS
    semester = [(str(i), str(i)) for i in range(1, 9)]

    # FORMS FIELDS
    yearOfJoining = forms.ModelChoiceField(queryset=Student.objects.values_list('yearOfJoining', flat=True).distinct(
    ).order_by('yearOfJoining'), to_field_name='yearOfJoining', empty_label="Select Year Of Joining")
    semester = forms.ChoiceField(choices=semester, required=True)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all().order_by(
        'branchCode'), empty_label="select Branch")
