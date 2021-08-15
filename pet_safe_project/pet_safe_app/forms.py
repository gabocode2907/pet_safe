from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Pet 

class PetImageForm(forms.ModelForm):
    class Meta:
        model = Pet 
        fields = ('pet_image',)
    #save the current model instance to the database and return the object
    #def save(self, commit=True):
    #    pet_image = super().save(commit=True)
    #    return pet_image


    