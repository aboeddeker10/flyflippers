from django.forms import ModelForm
from .models import Item
from .models import Photo
from django import forms
from .models import *

CONDITION_CHOICES = (
    ("New"),
    ("Like New"),
    ("Good"),
    ("Average"),
    ("Below Average"),
    
)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'

# class ItemForm(forms.Form):
#     name = forms.CharField(max_length=45)
#     description = forms.CharField(max_length=200)
#     price = forms.CharField(max_length=15)
#     condition = forms.CharField(max_length=25)
#     location = forms.CharField(max_length=45) #city, ST
#     poster = forms.ModelChoiceField() 