from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('start/',views.login),
    path('register/',views.register),
    path('admin/',views.admin),
    path('add/role/',views.addRole),
    path('add/gender/',views.addGender),
#     path('signin/',views.signin),
#     path('logout/',views.logout),
#     path('add/client/',views.addClient),
#     path('home/',views.home),
#     path('add/user/',views.addUser),

#     path('add/especialidad/',views.addEspecialidad),

#     path('add/hora/',views.addHora),
#     path('tab/type/<int:pk>',views.tabRequest),
#     path('del_user/<int:pk>',views.deleteUser),
#     path('edit_user/<int:pk>',views.editUser),
#     path('edit_profile/<int:pk>',views.editProfile),
#     path('new/appointment/',views.addAppointment),
# # Json path to load dropdown
#     path('esp-json/', views.get_json_esp_data, name='esp-json'),
#     path('tab/type/user-json/<int:pk>/', views.get_json_user_data, name='user-json'),
    
]