from django.db import models
from django.db.models.fields import CharField, DateField, DateTimeField, DecimalField, EmailField, IntegerField, PositiveSmallIntegerField, SmallIntegerField, TextField, TimeField
from datetime import date
import re,bcrypt
from django.utils.text import slugify
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey
from django.db.models.deletion import CASCADE
from pet_safe_app import civalidator


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$') #e-mail validations

class ClinicValidator(models.Manager):
    def newClinic_validator(self, postData):
        clinic_errors = {}
        try:
            val_email = Clinic.objects.get(clinic_email=postData['clinic_email'])
            if postData['clinic_email'] == val_email.clinic_email:
                clinic_errors['clinic_email'] = "La cuenta de correo electronico ya se encuentra en uso!!"
        except:
            if len(postData['clinic_address']) == 0:
                clinic_errors['clinic_address'] = "Debe ingresar una direccion!"
            elif len(postData['clinic_name']) == 0:
                clinic_errors['clinic_name'] = "Debe ingresar un nombre!!"
            elif not EMAIL_REGEX.match(postData['clinic_email']):   
                clinic_errors['clinic_email'] = "e-mail invalido!!"
            else:
                pass
        return clinic_errors

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
    def update_validator(self, postData):
        errors = {}
        if len(postData['direccion']) == 0:
            errors['direccion'] = "Debe ingresar una direccion!"
        if len(postData['fname']) == 0:
            errors['fname'] = "Debe ingresar un nombre!!"
        if len(postData['lname']) == 0:
            errors['lname'] = "Debe ingresar un apellido!!"
        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "e-mail invalido!!"
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

class PetType(models.Model):
    specie = CharField(max_length=50)
    created_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)

class Vaccine(models.Model):
    vaccine_name = CharField(max_length=50)
    vaccine_date = DateField()
    vaccine_next_date = DateField()
    created_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)

class Pet(models.Model):
    pet_name = CharField(max_length=50)
    pet_age = PositiveSmallIntegerField(null=True, blank=True)
    pet_birth_date = DateField(null=True, blank=True)
    pet_type = ForeignKey(PetType,related_name='pets',on_delete=CASCADE)
    pet_breed = CharField(max_length=50)
    pet_gender = CharField(max_length=6) 
    pet_weight = DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    pet_color = CharField(max_length=50)
    description = CharField(max_length=250)
    is_lost = SmallIntegerField()
    pet_image = ImageField(upload_to='pet_image/', blank=True)
    pet_owner = ForeignKey(User, related_name='pets_owner', on_delete=CASCADE)
    vaccines = ForeignKey(Vaccine, related_name="pet_vaccines",on_delete=CASCADE,null=True)
    created_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)
    def __str__(self):
        return self.pet_name
    

class Clinic(models.Model):
    clinic_name = CharField(max_length=50)
    clinic_address = CharField(max_length=150)    
    clinic_hphone = PositiveSmallIntegerField()
    clinic_cphone = PositiveSmallIntegerField()
    clinic_email = EmailField(max_length=100)
    created_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)
    objects = ClinicValidator()




