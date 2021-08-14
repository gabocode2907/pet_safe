from django.contrib import admin
from .models import Pet, Vaccine

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = [
        'pet_name', 'pet_age', 'pet_birth_date',
        'pet_type', 'pet_breed', 'pet_image'
        ]

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = [ 'vaccine_name']

# Register your models here.
