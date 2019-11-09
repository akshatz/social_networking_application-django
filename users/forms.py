from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

def past(value):
    if value > date.today():
        raise forms.ValidationError("Date cannot be of the future")

class DateInput(forms.DateInput):
    input_type = 'date'




class UserRegisterForm(UserCreationForm):
    dateofbirth = forms.DateField(label='Date of birth', widget=DateInput, validators=[past])

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'dateofbirth',
            'email'
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    dateofbirth = forms.DateField(widget=DateInput,  validators=[past])

    class Meta:
        model = User
        fields = [
            'email',
            'dateofbirth',
            'first_name',
            'last_name'
        ]
def past(value):
    if value > date.today():
        raise forms.ValidationError("Date cannot be of the future")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image'
        ]
def past(value):
    if value > date.today():
        raise forms.ValidationError("Date cannot be of the future")
    else:
        pass