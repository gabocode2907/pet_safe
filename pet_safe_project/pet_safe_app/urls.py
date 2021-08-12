from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('about/',views.about),
    path('contact/',views.contact),
    path('start/',views.login),
    path('register/',views.register),
    path('admin/',views.admin),
    path('add/role/',views.addRole),
    path('add/gender/',views.addGender),
    path('add/type/',views.addType),
    path('add/user/',views.addUser),
    path('signin/',views.signin),
    path('home/',views.home),
    path('edit/user/',views.editUser),
    path('logout/',views.logout),
    path('report/<int:pk>/',views.reportPet),
    path('found/',views.foundPet),
    path('found/pet/',views.foundPet),
    path('add/pet/',views.addPet),
    path('add/petUser/',views.addPetUser),
    path('mypet/<int:pet_id>',views.mypet),
    path('add/clinic/', views.addClinic),
    path('clinic/form/', views.clinicForm),
    path('list/clinic/', views.listClinics),
    path('view/<int:pk>',views.viewClinic),
]