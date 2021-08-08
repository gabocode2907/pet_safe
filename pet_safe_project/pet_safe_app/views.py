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

def signin(request):
    if request.method == "POST":
        login_errors = User.objects.login_validator(request.POST)
        if len(login_errors) > 0:
            for key, value in login_errors.items():
                messages.error(request,value,extra_tags='login')
            return redirect('/signin/')
        logged_user = User.objects.get(email=request.POST['email'])
        request.session['logged_user'] = logged_user.id
        request.session['user_role'] = logged_user.rol.id
        return redirect('/home/') 
    return redirect('/')

def addRole(request):
    # if "logged_user" not in request.session:
    #     messages.error(request,"There is not logged user!! Log in first!")
    #     return redirect('/')
    if request.method == "POST":
        Rol.objects.create(rol=request.POST['role'])
    return redirect('/admin/')

def addGender(request):
    if request.method == "POST":
        Gender.objects.create(gender=request.POST['gender'])   
    return redirect('/admin/')

def  register(request):
    genders = Gender.objects.all()
    context = {
        'genders' : genders
    }
    print(context)
    return render(request,'register.html',context)

def addUser(request):
    # if "logged_user" not in request.session:
    #     print("QUE CHUCHA PASA? HAY SESION?")
    #     messages.error(request,"There is not logged user!! Log in first!")
    #     return redirect('/')
    if request.method == "POST":
        errors = User.objects.new_user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value,extra_tags='register')
            return redirect('/register/')
        else:
            password = request.POST['pwd']
            pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            gender = Gender.objects.get(id=request.POST['sexo'])
            rol = Rol.objects.get(id='2')
            User.objects.create(fname=request.POST['fname'],lname=request.POST['lname'],cedula=request.POST['cedula'],direccion=request.POST['direccion'],hphone=request.POST['hphone'],cphone=request.POST['cphone'],rol=rol,sexo=gender,dob=request.POST['dob'],email=request.POST['email'],password=pw_hash)
            messages.success(request, 'Usuario creado correctamente!',extra_tags='success')
            return redirect('/register/')
    return redirect('/register/')

def admin(request):
    roles = Rol.objects.all()
    users = User.objects.all()
    context = {
        'roles' : roles,
        'users' : users,
    }
    return render(request,'admin.html',context)

def home(request):
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/')
    if request.method == "POST":
        errors = User.objects.new_user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value,extra_tags='nuser')
            return redirect('/signin/')
    logged_user_level = User.objects.get(id=request.session['logged_user'])
    all_users = User.objects.all()
    context = {
        'all_users' : all_users,
        'logged_user_level' : logged_user_level
    }   
    return render(request,'home.html',context)

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

# def logout(request):
#     request.session.flush()
#     return redirect('/')