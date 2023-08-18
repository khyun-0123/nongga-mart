from django import forms
from django.contrib.auth.forms import AuthenticationForm


class Login_Form(forms.Form):
    email = forms.EmailField(max_length=100, required=False)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    