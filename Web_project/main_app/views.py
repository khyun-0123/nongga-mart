from django.shortcuts import render, redirect
import supabase_py
from django.contrib.auth.decorators import permission_required
from supabase_py import create_client
from django.conf import settings
from django.urls import reverse
from .models import post_data_model
from django.http import JsonResponse,HttpResponse
import requests
import json
from django.contrib.auth.models import User
from main_app.permissions import UserClass
from django.contrib.auth.decorators import login_required
from datetime import datetime   
#upgrade

def upgrade_field():
    post_data_model.objects.all().delete()
    supa_url = "https://zxqrqhzzmaxqcrnrurxh.supabase.co/rest/v1/posts?select=*"
    header = {
        "apikey": settings.SUPABASE_API_KEY2,
        "Authorization": f"Bearer {settings.SUPABASE_API_KEY2}"
    }
    response = requests.get(supa_url, headers=header)
    print(response)
    response_json = response.json()
    for item in response_json:
        post, created = post_data_model.objects.get_or_create(
            Post_ID_field=item['id'],
            defaults={
                'title_field': item["title"],
                'content_field': item["content"],
                'User_ID_field': item["user_id"],
                'Time_field': item["created_at"],
            }
        )
    
    return

@login_required
def Main_pase(request):
    upgrade_field()
    data = post_data_model.objects.all()  
    return render(request, "mainpase.html",{"data" : data})


#delet button

def delet_db_fn(post_data):
    SUPABASE_URL = f'https://zxqrqhzzmaxqcrnrurxh.supabase.co/rest/v1/posts?id=eq.{post_data}'
    headers = {
        'apikey': settings.SUPABASE_API_KEY2,
        "Authorization": f"Bearer {settings.SUPABASE_API_KEY2}"
    }
    response = requests.delete(SUPABASE_URL, headers=headers)
    return response

@login_required
def delet_to_fn(request):
    if request.method == "POST":
        try:
            data = json.loads(request.POST.get("data"))
            user=request.user
            user_id=data["user_id"]
            post_data=data["post_id"]
            if user.has_perm("main_app.user"):
                now_login_data = request.user.username
                if user_id==now_login_data:
                    data_to_delete = post_data_model.objects.get(Post_ID_field=post_data)
                    data_to_delete.delete()
                    response = delet_db_fn(post_data)
                    print(response)
                    if response.status_code==204:
                        return redirect("main")
            elif user.has_perm("main_app.manager"):
                data_to_delete = post_data_model.objects.get(Post_ID_field=post_data)
                data_to_delete.delete()
                delet_db_fn(post_data)
                return redirect("main")
                

            return render(request, "mainpase.html",{"data" : data})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@login_required
def modify(request):
    if request.method == "GET":
        try:
            user=request.user
            user_id = request.GET.get("user_id")
            post_id = request.GET.get("post_id")
            post_text = request.GET.get("post_text")
            title = request.GET.get("title")
            context = {
                "user_id": user_id,
                "post_id": post_id,
                "post_text": post_text,
                "title": title
            }
            print(context)
            print("ㅡㅡㅡㅡㅡㅡㅡㅡ")
            if user.has_perm("main_app.user"):
                now_login_data = request.user.username
                if user_id==now_login_data:
                    return render(request, 'modify.html',{"context" : context})
                else:
                    print("실패")
            elif user.has_perm("main_app.manager"):
                return render(request, 'modify.html',{"context" : context})
            elif user.has_perm("main_app.admin"):
                print("어드민")
            else:
                print("나가")
            return HttpResponse("POST 요청 처리 완료1")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return redirect("main")

def modifyingsupapos(post_id, value):
    SUPABASE_URL = f'https://zxqrqhzzmaxqcrnrurxh.supabase.co/rest/v1/posts?id=eq.{post_id}'
    HEADERS = {
        'apikey': settings.SUPABASE_API_KEY2,
        'Authorization': f'Bearer {settings.SUPABASE_API_KEY2}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    DATA1 = {
        "content": value  
    }
    response = requests.patch(SUPABASE_URL, headers=HEADERS, json=DATA1)
    return response.status_code

def modifyingsupatit(post_id, value):
    SUPABASE_URL = f'https://zxqrqhzzmaxqcrnrurxh.supabase.co/rest/v1/posts?id=eq.{post_id}'
    
    HEADERS = {
        'apikey': settings.SUPABASE_API_KEY2,
        'Authorization': f'Bearer {settings.SUPABASE_API_KEY2}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    DATA = {
        "title": value 
    }
    response = requests.patch(SUPABASE_URL, headers=HEADERS, json=DATA)

    return response.status_code

def modifying(request):
    title = request.GET.get("title")
    post = request.GET.get("post")
    post_id = request.GET.get("post_id")

    status_code_post = modifyingsupapos(post_id, post)
    status_code_title = modifyingsupatit(post_id, title)
    print(status_code_title)
    if status_code_post == 204 and status_code_title == 204:
        return redirect("main")
    else:
        return HttpResponse("Failed to update data")
