from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ContactUs(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(max_length=500)
    email = forms.EmailField()
