from .models import  User,Rol,Gender
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls.conf import include
from django.contrib import messages
import bcrypt
from datetime import date
from pprint import pp, pprint
from datetime import datetime

def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'signin.html')

# def signin(request):
#     if request.method == "POST":
#         if request.POST['log_type'] == "dr":
#             login_errors = User.objects.login_validator(request.POST)
#             if len(login_errors) > 0:
#                 for key, value in login_errors.items():
#                     messages.error(request,value,extra_tags='login')
#                 return redirect('/login/')
#             logged_user = User.objects.get(email=request.POST['email'])
#             request.session['logged_user'] = logged_user.id
#             request.session['user_role'] = logged_user.rol_id.id
#             return redirect('/home/') 
#         if request.POST['log_type'] == "ct":
#             login_errors = Client.objects.ct_login_validator(request.POST)
#             if len(login_errors) > 0:
#                 for key, value in login_errors.items():
#                     messages.error(request,value,extra_tags='login')
#                 return redirect('/login/')
#             logged_user = Client.objects.get(email=request.POST['email'])
#             request.session['logged_user'] = logged_user.id
#             request.session['user_role'] = "client"
#             return redirect('/home/')
#     return redirect('/')

def addRole(request):
    # if "logged_user" not in request.session:
    #     messages.error(request,"There is not logged user!! Log in first!")
    #     return redirect('/')
    if request.method == "POST":
        Role.objects.create(rol=request.POST['role'])
    return redirect('/admin/')

def addGender(request):
    if request.method == "POST":
        Gender.objects.create(gender=request.POST['gender'])   
    return redirect('/admin/')

# def addEspecialidad(request):
#     if request.method == "POST":
#         Especialidad.objects.create(especialidad=request.POST['especialidad'])   
#     return redirect('/admin/')

# def addHora(request):
#     if request.method == "POST":
#         user = User.objects.get(id=request.POST['users'])
#         horas = request.POST['hora']
#         Hora.objects.create(horas=horas,usuario=user)   
#     return redirect('/admin/')

def  register(request):
    # genders = Gender.objects.all()
    # context = {
    #     'genders' : genders
    # }
    # print(context)
    # if request.method == "POST":
    #     errors = User.objects.new_client_validator(request.POST)
    #     if len(errors) > 0:
    #         for key, value in errors.items():
    #             messages.error(request,value,extra_tags='register')
    #         return redirect('/add/client/')
    #     else:
    #         password = request.POST['pwd']
    #         pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
    #         gender = Gender.objects.get(id=request.POST['sexo'])
    #         Client.objects.create(fname=request.POST['fname'],lname=request.POST['lname'],cedula=request.POST['cedula'],direccion=request.POST['direccion'],hphone=request.POST['hphone'],cphone=request.POST['cphone'],sexo=gender,dob=request.POST['dob'],email=request.POST['email'],password=pw_hash)
    #         messages.success(request, 'Usuario creado correctamente! Puede iniciar sesion!',extra_tags='success')
    #         return redirect('/login/')
    return render(request,'register.html')

# def addUser(request):
#     # if "logged_user" not in request.session:
#     #     print("QUE CHUCHA PASA? HAY SESION?")
#     #     messages.error(request,"There is not logged user!! Log in first!")
#     #     return redirect('/')
#     if request.method == "POST":
#         errors = User.objects.new_user_validator(request.POST)
#         if len(errors) > 0:
#             for key, value in errors.items():
#                 messages.error(request,value,extra_tags='nuser')
#             return redirect('/admin/')
#         else:
#             password = request.POST['pwd']
#             pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
#             rol_id = Role.objects.get(id=request.POST['role'])
#             especialidad = Especialidad.objects.get(id=request.POST['especialidad'])
#             User.objects.create(especialidad=especialidad,sfname=request.POST['sfname'],slname=request.POST['slname'],email=request.POST['email'],password=pw_hash,rol_id=rol_id)
#             messages.success(request, 'Usuario creado correctamente!',extra_tags='success')
#             return redirect('/admin/')
#     return redirect('/admin/')

def admin(request):
    roles = Rol.objects.all()
    users = User.objects.all()
    context = {
        'roles' : roles,
        'users' : users,
    }
    return render(request,'admin.html',context)

# def home(request):
#     if "logged_user" not in request.session:
#         messages.error(request,"There is not logged user!! Log in first!")
#         return redirect('/')
#     if request.method == "POST":
#         errors = User.objects.new_user_validator(request.POST)
#         if len(errors) > 0:
#             for key, value in errors.items():
#                 messages.error(request,value,extra_tags='nuser')
#             return redirect('/signin/')
#     logged_user_level = User.objects.get(id=request.session['logged_user'])
#     all_users = User.objects.all()
#     context = {
#         'all_users' : all_users,
#         'logged_user_level' : logged_user_level
#     }   
#     return render(request,'home.html',context)

# def tabRequest(request,pk):
#     horarios = Hora.objects.all()
#     context = {
#     'tab' : pk,
#     'horarios' : horarios
#     }
#     return render(request,'home.html',context)

# def deleteUser(request,pk):
#     usr_to_del = User.objects.get(id =pk)
#     usr_to_del.delete()
#     return redirect('/dashboard/')

# def editUser(request,pk):
#     if "logged_user" not in request.session:
#         messages.error(request,"There is not logged user!! Log in first!")
#         return redirect('/')
#     if request.method == "POST":
#         user_to_edit = User.objects.get(id=pk)
#         if request.POST['update_type'] == 'usr':
#             errors = User.objects.form_validator(request.POST)
#             if len(errors) > 0:
#                 for key, value in errors.items():
#                     messages.error(request,value)
#                 return redirect('/edit_user/'+str(pk))
#             else:
#                 user_to_edit.email = request.POST['email']
#                 user_to_edit.fname = request.POST['fname']
#                 user_to_edit.lname = request.POST['lname']
#                 user_to_edit.user_level = request.POST['user_level']
#                 user_to_edit.save()
#                 return redirect('/dashboard/')
#         if request.POST['update_type'] == 'pwrd':
#             errors = User.objects.form_validator(request.POST)
#             if len(errors) > 0:
#                 for key, value in errors.items():
#                     messages.error(request,value)
#                 return redirect('/edit_user/'+str(pk))
#             else:
#                 password = request.POST['password']
#                 pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
#                 user_to_edit.password = pw_hash
#                 user_to_edit.save()
#                 return redirect('/dashboard/')
#     usr_to_edit = User.objects.get(id=pk)
#     logged_user_level = User.objects.get(id=request.session['logged_user']).user_level
#     context = {
#         'usr_to_edit' : usr_to_edit,
#         'logged_user_level' : logged_user_level
#     }
#     return render(request,'edit_user.html',context)

# def editProfile(request,pk):
#     if "logged_user" not in request.session:
#         messages.error(request,"There is not logged user!! Log in first!")
#         return redirect('/')
#     if request.method == "POST":
#         user_to_edit = User.objects.get(id=pk)
#         if request.POST['update_type'] == 'usr':
#             errors = User.objects.form_validator(request.POST)
#             if len(errors) > 0:
#                 for key, value in errors.items():
#                     messages.error(request,value)
#                 return redirect('/edit_profile/'+str(pk))
#             else:
#                 user_to_edit.email = request.POST['email']
#                 user_to_edit.fname = request.POST['fname']
#                 user_to_edit.lname = request.POST['lname']
#                 user_to_edit.save()
#                 return redirect('/dashboard/')
#         if request.POST['update_type'] == 'pwrd':
#             errors = User.objects.form_validator(request.POST)
#             if len(errors) > 0:
#                 for key, value in errors.items():
#                     messages.error(request,value)
#                 return redirect('/edit_profile/'+str(pk))
#             else:
#                 password = request.POST['password']
#                 pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
#                 user_to_edit.password = pw_hash
#                 user_to_edit.save()
#                 return redirect('/dashboard/')
#     usr_to_edit = User.objects.get(id=pk)
#     logged_user_level = User.objects.get(id=request.session['logged_user']).user_level
#     context = {
#         'usr_to_edit' : usr_to_edit,
#         'logged_user_level' : logged_user_level
#     }
#     return render(request,'edit_profile.html',context)

# def addAppointment(request):
#     add_desc = User.objects.get(id=request.POST['desc_usr_id'])
#     add_desc.description = request.POST['description']
#     add_desc.save()
#     return redirect('/dashboard/')

# def logout(request):
#     request.session.flush()
#     return redirect('/')



# # This section will allow the dropdown loading 
# # def main_view(request):
# #     qs = Car.objects.all()
# #     return render(request, 'orders/main.html', {'qs':qs})

# # def traditional_view(request):
# #     qs1 = Car.objects.all()
# #     qs2 = Model.objects.all()
# #     return render(request, 'orders/t.html', {'qs1':qs1, 'qs2':qs2})

# def get_json_esp_data(request):
#     qsj = list(Especialidad.objects.values())
#     return JsonResponse({'data':qsj})

# # def get_json_user_data(request, *args, **kwargs):
# #     selected_car = kwargs.get('esp-data')
# #     obj_models = list(Model.objects.filter(car__name=selected_car).values())
# #     return JsonResponse({'data':obj_models})

# # def get_json_user_data(request, *args, **kwargs):
# #     selected_esp = kwargs.get('esp-data')
# #     print(selected_esp)
# #     obj_users = list(User.objects.filter(especialidad__id=selected_esp).values())
# #     return JsonResponse({'data':obj_users})
# def get_json_user_data(request, pk):
#     selected_esp = pk
#     print(selected_esp)
#     obj_users = list(User.objects.filter(especialidad__id=selected_esp).values())
#     return JsonResponse({'data':obj_users})

# # def create_order(request):
# #     if request.is_ajax():
# #         car = request.POST.get('car')
# #         car_obj = Car.objects.get(name=car)
# #         model = request.POST.get('model')
# #         model_obj = Model.objects.get(name=model, car__name=car_obj.name)
# #         Order.objects.create(car=car_obj, model=model_obj)
# #         return JsonResponse({'created': True})
# #     return JsonResponse({'created': False})

# def addToCal(request):
#     CLIENT_SECRET_FILE = 'client_secret_file.json'
#     API_NAME = 'calendar'
#     API_VERSION = 'v3'
#     SCOPES = ['https://www.googleapis.com/auth/calendar']

#     service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
#     calendarID = 'abdontipan@gmail.com'
#     # CREATE AN EVENT

#     colors = service.colors().get().execute()
#     pprint(colors)
#     hour_adjustment = -5
#     event_request_body = {
#         'start' : {
#             'dateTime' : convert_to_RFC_datetime(2021,7,29,15 + hour_adjustment,30),
#             'timeZone' : 'Asia/Taipei'
#         },  
#         'end':{
#             'dateTime' : convert_to_RFC_datetime(2021,7,29,16 + hour_adjustment,30),
#             'timeZone' : 'America/Guayaquil'
#         },
#         'summary' : 'Family Lunch',
#         'description' : 'Having lunc with parents',
#         'colorID' : 5,
#         'status' : 'confirmed',
#         'transparency' : 'opaque',
#         'visibility' : 'public',
#         'location' : 'Inglaterra N31-210 y Av. Mariana de Jesus',
#         'attendees' : [
#             {
#                 'displayName' : 'Gabo',
#                 'comment' : 'test comment',
#                 'email' : 'abdontipan@gmail.com',
#                 'optional' : False,
#                 'organizer' : True,
#                 'responseStatus' : 'accepted'
#             }
#         ],
#         # 'creator' : {

#         # },
#         # 'organizer' : {

#         # }
#     } 

#     maxAttendee = 5
#     sendNotification = True
#     sendUpdate = 'none'
#     suppportAttachments = True

#     response = service.events().insert(
#     calendarId=calendarID,
#     maxAttendees = maxAttendee,
#     sendNotifications = sendNotification,
#     supportsAttachments = suppportAttachments,
#     sendUpdates = sendUpdate,
#     body = event_request_body
#     ).execute()

#     pprint(response)