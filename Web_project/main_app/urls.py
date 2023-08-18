# main_app/urls.py
from django.urls import path
# from main_app.views import delet_to_fn
from main_app.views import delet_to_fn,modify,modifying


app_name = "main_app"

urlpatterns = [
    path("deletdata/", delet_to_fn, name='deleted'),
    path("modify_ready/", modify, name='modifyready'),
    path("modify/", modifying, name='modify'),
]