
from django.db import models
import re
from datetime import datetime
from .models import *
from django.core.exceptions import ValidationError
import bcrypt
from cloudinary.models import CloudinaryField

# Create your models here.

CONDITION_CHOICES = [
    ('New'),
    ('Excellent'),
    ('Lightly Used'),
    ('Average'),
    ('Below Average'),
]

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be at least 2 characters"
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters"
        UserRegex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not UserRegex.match(postData['email']):
            errors['email'] = "This is not a valid email address"
        if postData['password'] != postData['confirm']:
            errors['confirm'] = "Passwords do not match"
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['emailAlreadyExists'] = "This email is already in use"

        return errors
    
    def login_validator(self, postData):
            errors1 = {}
            LoginUser = User.objects.filter(email=postData['logemail'])
            if len(LoginUser) > 0:
                # checking if the login password used matches the user password stored in the database
                if bcrypt.checkpw(postData['logpassword'].encode(), LoginUser[0].password.encode()):
                    print("password matches")
                else:
                    errors1['logpassword'] = "That email and password combo is incorrect"
            else:
                errors1['logemail'] = "That email is already associated with another account or incorrectly entered"

            return errors1

        
def validateLengthGreaterThanTwo(value):
    if len(value) < 3:
        raise ValidationError(
            '{} must be longer than: 2'.format(value)
        )
        
    
# class ItemManager(models.Manager):
#     def basic_validator(self, postData):

#         errors = {}

#         if len(postData['name']) < 4:
#             errors['name'] = "The Name of Item field should include at least 4 Characters"

#         if len(postData['description']) < 15:
#             errors['description'] = "The Description should be at least 15 characters in length"
            
#         if len(postData['condition']) < 3:
#             errors['condition'] = "Condition should be at least 3 characters in length"

#         if len(postData['location']) < 4:
#             errors['location'] = "The Location field should include at least 4 Characters"

#         return errors
    
    
    
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    # def __repr__(self):
    #     return '{}'.format(self.first_name)
    def __str__(self):
        return self.first_name
    
class Item(models.Model):
    name = models.CharField(max_length=100, validators=[validateLengthGreaterThanTwo])
    description = models.TextField(validators=[validateLengthGreaterThanTwo])
    price = models.CharField(max_length=15)
    condition = models.CharField(max_length=25, validators=[validateLengthGreaterThanTwo])
    location = models.CharField(max_length=45, validators=[validateLengthGreaterThanTwo]) #city, ST
    image = CloudinaryField('image', null=True)
    poster = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorite = models.BooleanField(default=False)
    # objects = ItemManager()
    
    
# class Photo(models.Model):
#     image = CloudinaryField('image')