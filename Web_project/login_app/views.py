from django.shortcuts import render, redirect
import requests
from django.http import HttpResponseServerError
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.models import User
from .forms import Login_Form
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from main_app.permissions import UserClass

def fetch_supabase_users(access_token):
    url =  'https://zxqrqhzzmaxqcrnrurxh.supabase.co/auth/v1/user'
    headers = {
        "apikey": settings.SUPABASE_API_KEY,
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json=response.json()
        email_data = response_json.get('email')
        ID_data = response_json.get('id')
        return email_data,ID_data
    else:
        return None

    
    
def login_to_supabase(user_email, user_password):
    supabase_url = 'https://zxqrqhzzmaxqcrnrurxh.supabase.co/auth/v1/token?grant_type=password'
    data = {
        "email": user_email,
        "password": user_password
    }
    headers = {
        "apikey": settings.SUPABASE_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(supabase_url, headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        access_token = response_json.get('access_token')
        return response, access_token
    else:
        return response, None

def Login_pase(request):
    if request.method == 'POST':
        form = Login_Form(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_password = form.cleaned_data['password']
            response,access_token = login_to_supabase(user_email, user_password)
            if response.status_code == 200 and access_token:
                Email, UID=fetch_supabase_users(access_token)
                user, created = User.objects.get_or_create(username=UID, email=Email)
                user.set_password("basepassword")
                user.save()
                if user is not None:
                    user = User.objects.get(username=UID)
                    permission = Permission.objects.get(codename="user")
                    user.user_permissions.add(permission)
                    login(request, user)
                    return redirect("main")
                else:
                    return HttpResponseServerError("로그인 실패")
            else:
                return HttpResponseServerError("로그인 실패")
    else:
        form = Login_Form()
    return render(request, "login.html", {'form': form})
