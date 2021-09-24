from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import Widget
from .models import Item
from django import forms
from .models import *



class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['poster', 'favorite']
        CONDITION_CHOICES = (
            ("new", "New"),
            ("like new", "Like New"),
            ("minor wear", "Minor Wear"),
            ("obvious wear", "Obvious Wear"),
            ("functional", "Functional"),
        )
        widgets = {
            'condition': forms.Select(choices=CONDITION_CHOICES)
        }
        
# class ConditionForm(forms.Form):
#     condition = forms.ChoiceField(choices = CHOICES)  
    
    
    
        # Widget = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'description': forms.Textarea(attrs={'class': 'form-control'}),
        #     'price': forms.TextInput(attrs={'class': 'form-control'}),
        #     'condition': forms.TextInput(attrs={'class': 'form-control'}),
        #     'location': forms.TextInput(attrs={'class': 'form-control'}),
        #     'image': forms.ImageField(attrs={'class': 'form-control'}),
        #     'poster': forms.Select(attrs={'class': 'form-control'}),
        # }



# class ItemForm(forms.Form):
#     name = forms.CharField(max_length=45)
#     description = forms.CharField(max_length=200)
#     price = forms.CharField(max_length=15)
#     condition = forms.CharField(max_length=25)
#     location = forms.CharField(max_length=45) #city, ST
#     poster = forms.ModelChoiceField() 