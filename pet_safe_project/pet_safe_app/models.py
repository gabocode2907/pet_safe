from django.db import models
from django.db.models.fields import CharField, DateField, DateTimeField, EmailField, IntegerField, TimeField
from datetime import date
import re,bcrypt
from django.db.models.fields.related import ForeignKey
from django.db.models.deletion import CASCADE


class Rol(models.Model):
    rol = CharField(max_length=50)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Gender(models.Model):
    gender = CharField(max_length=20)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Client(models.Model):
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