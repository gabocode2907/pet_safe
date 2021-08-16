from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Pet 

class PetImageForm(forms.ModelForm):
    class Meta:
        model = Pet 
        fields = ('pet_image',)
        exclude = ('pet_owner',)



    