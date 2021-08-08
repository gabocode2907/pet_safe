from django.db import models
from django.db.models.fields import CharField, DateField, DateTimeField, DecimalField, EmailField, IntegerField, PositiveSmallIntegerField, TextField, TimeField
from datetime import date
import re,bcrypt
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.deletion import CASCADE
from pet_safe_app import civalidator


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$') #e-mail validations

class RegistrationManager(models.Manager):
    def new_user_validator(self, postData):
        errors = {}
        try:
            val_email = User.objects.get(email=postData['email'])
            if postData['email'] == val_email.email:
                errors['email'] = "La cuenta de correo electronico ya se encuentra en uso!!"
        except:
            if civalidator.ci_validator(postData['cedula']) == 0:
                errors['cedula'] = "Cedula no valida, ingrese nuevamnte"
            if len(postData['direccion']) == 0:
                errors['direccion'] = "Debe ingresar una direccion!"
            if len(postData['fname']) == 0:
                errors['fname'] = "Debe ingresar un nombre!!"
            if len(postData['lname']) == 0:
                errors['lname'] = "Debe ingresar un apellido!!"
            if not EMAIL_REGEX.match(postData['email']):   
                errors['email'] = "e-mail invalido!!"
            if postData['pwd'] != postData['cpwd']:
                    errors['cconfirm_password'] = "Las contraseñas no coinciden!!"
            else:
                if len(postData['pwd']) <8 or len(postData['cpwd']) <8:
                    errors['passwords'] = "La contraseña debe ser al menos de 8 caracteres!!"
        return errors
    def login_validator(self, postData):
        login_errors = {}
        try:
            val_email = User.objects.get(email=postData['email'])
            if postData['email'] == val_email.email:
                user = User.objects.get(email=postData['email'])
                if not bcrypt.checkpw(postData['pwd'].encode(),user.password.encode()):
                    login_errors['wrong_password'] = "Wrong Password, Try again!!"
                return login_errors
        except:
            login_errors['not_user'] = "User not registered, please register first!!"
        return login_errors
    def ct_login_validator(self, postData):
        login_errors = {}
        try:
            val_email = User.objects.get(email=postData['email'])
            if postData['email'] == val_email.email:
                user = User.objects.get(email=postData['email'])
                if not bcrypt.checkpw(postData['pwd'].encode(),user.password.encode()):
                    login_errors['wrong_password'] = "Wrong Password, Try again!!"
                return login_errors
        except:
            login_errors['not_user'] = "User not registered, please register first!!"
        return login_errors

class AppointmentManager(models.Manager):
    def appointment_validator(self, postData):
        appointment_errors = {}
        current_date = date.today()
        if len(postData['task']) == 0:
                appointment_errors['task'] = "You must enter a Task Name!!"
        if postData['date'] < current_date.strftime("%Y-%m-%d"):
                appointment_errors['date'] = "An appointment date cannot be in the past!!"
        return appointment_errors

class ClientManager(models.Manager):
    def appointment_validator(self, postData):
        appointment_errors = {}
        current_date = date.today()
        if len(postData['task']) == 0:
                appointment_errors['task'] = "You must enter a Task Name!!"
        if postData['date'] < current_date.strftime("%Y-%m-%d"):
                appointment_errors['date'] = "An appointment date cannot be in the past!!"
        return appointment_errors

class Rol(models.Model):
    rol = CharField(max_length=50)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Gender(models.Model):
    gender = CharField(max_length=20)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class User(models.Model):
    fname = CharField(max_length=50)
    lname = CharField(max_length=50)
    cedula = IntegerField(null=True)
    direccion = CharField(max_length=150)
    hphone = IntegerField()
    cphone = IntegerField()
    rol = ForeignKey(Rol, related_name="clients",on_delete=CASCADE)
    sexo = ForeignKey(Gender, related_name="clients",on_delete=CASCADE)
    dob = DateField()
    email = EmailField(max_length=100)
    password = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = RegistrationManager()

class vetRecord(models.Model):
    pet_name = CharField(max_length=50)
    pet_age = PositiveSmallIntegerField()
    pet_birth_date = DateField()
    pet_breed = CharField(max_length=50)
    pet_gender = CharField(max_length=6) 
    pet_weight = DecimalField(decimal_places=2, max_digits=5)
    pet_color = CharField(max_length=50)
    allergies = CharField(max_length=50)
    existing_conditions = CharField(max_length=250)
    description = CharField(max_length=250)
    diagnosis = CharField(max_length=250)
    pet_image = ImageField(upload_to='pet_image/')
    review_data = DateField() #fecha de revisión de la mascota
    test_performed = CharField(max_length=50) 
    test_results = CharField(max_length=50) #done, pendiente, etc
    action = CharField(max_length=250) #cuidados a la mascota que tendrá que llevar a cabo el cliente
    medication = CharField(max_length=250)
    comments = CharField(max_length=250) #aplica, no aplica, commentarios finales del veterinario
    pet_owner = ForeignKey(User, related_name='pets_owner', on_delete=CASCADE) #quizá seria adecuado que la mascota tenga varios dueños... manyTomany?
    rol = ManyToManyField(Rol, related_name='veterinarians')
    created_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)

class Clinic(models.Model):
    clinic_name = CharField(max_length=50)
    clinic_address = CharField(max_length=150)    
    clinic_hphone = PositiveSmallIntegerField()
    clinic_cphone = PositiveSmallIntegerField()
    rol = ManyToManyField(Rol, related_name='clinic_vets')
    clinic_email = EmailField(max_length=100)
    created_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)

class ImmunizationHistory(models.Model):
    year = PositiveSmallIntegerField()
    vaccine = CharField(max_length=250)
    pet_vaccine_hist = ForeignKey(vetRecord, related_name='pet_vaccines', on_delete=CASCADE)
    clinic_vaccine_hist = ForeignKey(Clinic, related_name='clinic_vaccines', on_delete=CASCADE)
    created_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)


