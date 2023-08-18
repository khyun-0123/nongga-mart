from django import forms
from django.contrib.auth.forms import AuthenticationForm


class Login_Form(forms.Form):
    title_form=models.CharField(max_length=200)
    content_form = forms.CharField(max_length=100)
    