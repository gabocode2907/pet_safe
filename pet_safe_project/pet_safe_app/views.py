from .models import  Pet, User,Rol,Gender,PetType,Clinic
from .forms import PetImageForm
from django.shortcuts import redirect, render
from django.contrib import messages
import bcrypt
from datetime import date
from pprint import pp, pprint
from datetime import datetime
from django.core.mail import send_mail

def index(request):
    genders = Gender.objects.all()
    context = {
        'genders' : genders
    }
    return render(request,'index.html',context)

def login(request):
    return render(request,'signin.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

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
    return redirect('/signin/')

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

def addType(request):
    if request.method == "POST":
        PetType.objects.create(specie=request.POST['pet_type'])   
    return redirect('/admin/')

def  register(request):
    genders = Gender.objects.all()
    context = {
        'genders' : genders
    }
    print(context)
    return render(request,'index.html',context)

def addUser(request):
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/signin/')
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
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/signin/')
    roles = Rol.objects.all()
    users = User.objects.all()
    logged_user = User.objects.get(id=request.session['logged_user'])
    context = {
        'roles' : roles,
        'users' : users,
        'logged_user' : logged_user
    }
    return render(request,'admin.html',context)

def home(request):
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/signin/')
    if request.method == "POST":
        errors = User.objects.new_user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value,extra_tags='nuser')
            return redirect('/signin/')
    logged_user = User.objects.get(id=request.session['logged_user'])
    all_pets = Pet.objects.filter(pet_owner=logged_user)
    context = {
        'logged_user' : logged_user,
        'all_pets' : all_pets
    }   
    return render(request,'home.html',context)

# def deleteUser(request,pk):
#     usr_to_del = User.objects.get(id =pk)
#     usr_to_del.delete()
#     return redirect('/dashboard/')

def editUser(request):
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/signin/')
    if request.method == "POST":
        user_to_edit = User.objects.get(id=request.session['logged_user'])
        errors = User.objects.update_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value,extra_tags='edituser')
            return redirect('/edit/user/')
        else:
            user_to_edit.fname = request.POST['fname']
            user_to_edit.lname = request.POST['lname']
            user_to_edit.direccion = request.POST['direccion']
            user_to_edit.hphone = request.POST['hphone']
            user_to_edit.cphone = request.POST['cphone']
            user_to_edit.sexo = Gender.objects.get(id=request.POST['sexo'])
            user_to_edit.dob = request.POST['dob']
            user_to_edit.email = request.POST['email']
            # user_to_edit.password = request.POST['pwd']
            user_to_edit.save()
            return redirect('/edit/user/')
    user_to_edit = User.objects.get(id=request.session['logged_user'])
    logged_user = User.objects.get(id=request.session['logged_user'])
    genders = Gender.objects.all()
    context = {
        'user_to_edit' : user_to_edit,
        'genders' : genders,
        'logged_user' : logged_user
    }
    context['up_date']= str(context['user_to_edit'].dob)
    return render(request,'edit_user.html',context)

def logout(request):
    request.session.flush()
    return redirect('/')

def reportPet(request,pk):
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/signin/')
    lost_pet = Pet.objects.get(id=pk)
    lost_pet.is_lost = 1
    lost_pet.save()
    return redirect('/home/')

def foundPet(request):
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/signin/')
    if request.method == "POST":
        lost_pet = Pet.objects.get(id=request.POST['pet_id'])
        pet_owner = User.objects.get(id=lost_pet.pet_owner.id)
        logged_user = User.objects.get(id=request.session['logged_user'])
        context = {
        'my_pet' : lost_pet,
        'logged_user' : logged_user,
        'pet_owner' : pet_owner
        }
        send_mail(
            'WE FOUND YOUR PET!!',
            'Your pet has been found by: ' + logged_user.fname + ' ' + logged_user.lname + ' Please contact him at: ' + '' + '0'+str(logged_user.cphone) + '.',
            'petsafe@med-import.com',
            [pet_owner.email],
            fail_silently=False,
        )
        # send_mail(
        #     'WE FOUND YOUR PET!!',
        #     'Your pet has been found by: ',
        #     'petsafe@med-import.com',
        #     ['gabriel2907@hotmail.com'],
        #     fail_silently=False,
        # )
        return render(request,'pet_found.html',context)
    logged_user = User.objects.get(id=request.session['logged_user'])
    context = {
        'logged_user' : logged_user
    }
    return render(request,'found_pet.html',context)

#================= Alexis / Despliega HTML Add Pet ===================
def addPet(request):
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/')
    
    logged_user = User.objects.get(id=request.session['logged_user'])
    pet_img_form = PetImageForm(data=request.GET)
    context = {
        'logged_user': logged_user,
        'all_petType': PetType.objects.all(),
        'pet_image': pet_img_form
    }
    return render(request,'add_pet.html',context)
#=====================================================================


#================= Alexis / Almacena Info Add Pet ====================
def addPetUser(request):
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/')
    
    user = User.objects.get(id=request.session['logged_user'])
    pet_name = request.POST.get("pet_name")
    # pet_age = request.POST.get("pet_age")
    pet_birth_date = request.POST.get("pet_birth_date")
    pet_type = PetType.objects.get(id=request.POST.get("pet_type"))
    pet_breed = request.POST.get("pet_breed")
    pet_gender = request.POST.get("pet_gender")
    pet_weight = request.POST.get("pet_weight")
    pet_color = request.POST.get("pet_color")
    description = request.POST.get("description")
    is_lost = request.POST.get("is_lost")
    #pet_image = request.POST.get("pet_image")
    pet_owner = User.objects.get(id=request.session['logged_user'])

    pet_image = PetImageForm(data=request.POST)
    pet_image.save(commit=False)
    pet_image.pet_owner = pet_owner
    pet_image.save()
    print("**********************", pet_image)
    # vaccines = request.POST.get("vaccines")


    if len(pet_name) <2:
        messages.error(request, 'Your Pet Name must be at least 2 characters')
        return redirect('/add/pet/')

    # if len(pet_age) <1:
    #     messages.error(request, 'Please insert your Pet Age')
    #     return redirect('/add/pet/')

    if len(pet_birth_date ) <1:
        messages.error(request, 'Please insert your Pet Birth Day')
        return redirect('/add/pet/')

    if len(pet_breed) <1:
        messages.error(request, 'Please select your Pet Breed')
        return redirect('/add/pet/')

    if len(pet_weight) <1:
        messages.error(request, 'Please insert your Pet Weight')
        return redirect('/add/pet/')

    if len(pet_color) <1:
        messages.error(request, 'Please insert your Pet Color')
        return redirect('/add/pet/')
    
    if len(description) <1:
        messages.error(request, 'Please insert a short description of your pet')
        return redirect('/add/pet/')

    #if len(pet_image) <1:
    #    messages.error(request, 'Please upload your Pet Photo')
    #    return redirect('/add/pet/')
    
    # if len(vaccines) <1:
    #     messages.error(request, 'Please insert vaccines applied to your Pet')
    #     return redirect('/add/pet/')


    fecha_dt = datetime.strptime(pet_birth_date, '%Y-%m-%d')
    def calculate_age(born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    pet_age = calculate_age(fecha_dt)
    # print('La edad de la Mascota es:',pet_age)


    vaccines = '' # Realizar en tabla de las vacunas
    is_lost = 0 # Si es cero mascota recién creada y NO PERDIDA, si es 1 para mascota perdida

    Pet.objects.create(
        pet_name = pet_name,
        pet_age = pet_age,
        pet_birth_date = pet_birth_date,
        pet_type = pet_type,
        pet_breed = pet_breed,
        pet_gender = pet_gender,
        pet_weight = pet_weight,
        pet_color = pet_color,
        description = description,
        is_lost = is_lost,
        pet_image = pet_image,
        pet_owner = pet_owner,
        # vaccines = vaccines # Revisar
        )
    print('\n\n**************\nFunción Cumplida\n\n**************')
    return redirect('/home/')
#=====================================================================

#================= Alexis / My Pet ===================================
def mypet(request, pet_id):
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/')

    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'my_pet': Pet.objects.get(id=pet_id)
    }

    return render(request,'mypet.html',context)
#=====================================================================

################## MARCELO #############################3
def clinicForm(request):
    return render(request, 'register_clinic.html')

def addClinic(request):
    if "logged_user" not in request.session:
        messages.error(request,"There is not logged user!! Log in first!")
        return redirect('/')
    if request.method == "POST":
        errors = Clinic.objects.newClinic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value,extra_tags='register')
            return redirect('/admin/')
        else:
            Clinic.objects.create(
                clinic_name=request.POST['clinic_name'],
                clinic_address=request.POST['clinic_address'],
                clinic_hphone=request.POST['clinic_hphone'],
                clinic_cphone=request.POST['clinic_cphone'],
                clinic_email=request.POST['clinic_email'],
                )
            messages.success(request, 'Clínica creada correctamente!',extra_tags='success')
            return redirect('/admin/')
    return redirect('/admin/')

def listClinics(request):
    if "logged_user" not in request.session:
            messages.error(request,"There is not logged user!! Log in first!")
            return redirect('/')
    context = {
        'all_clinics' : Clinic.objects.all(),
        'logged_user' : User.objects.get(id=request.session['logged_user'])
    }

    return render(request, 'list_clinics.html',context)
def viewClinic(request,pk):
    if "logged_user" not in request.session:
            messages.error(request,"There is not logged user!! Log in first!")
            return redirect('/')
    context = {
        'clinic' : Clinic.objects.get(id=pk),
        'logged_user' : User.objects.get(id=request.session['logged_user'])
    }
    return render(request, 'view_clinic.html',context) 
######################## MARCELO  #########################################################