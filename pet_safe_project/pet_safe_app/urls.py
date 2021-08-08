from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('start/',views.login),
    path('register/',views.register),
    path('admin/',views.admin),
    path('add/role/',views.addRole),
    path('add/gender/',views.addGender),
    path('add/user/',views.addUser),
    path('signin/',views.signin),
    path('home/',views.home),
#     path('logout/',views.logout),
    
]