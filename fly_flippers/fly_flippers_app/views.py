from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def process(request):  # handling form process data by adding info to database then redirecting, never render on POST
    if request.method == "POST":
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hashedpw = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt()).decode()
            print(request.POST['password'])
            print(hashedpw)
            newUser = User.objects.create(
                first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashedpw)
            # keep session upon login and registration exactly the same ['user']
            request.session['user'] = newUser.id
            return redirect('/success')
    else:
        return redirect('/')
    

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        "new_user": User.objects.last(),
    }
    return render(request, 'success.html', context)

def login(request):  # sends to dashboard page if successful login attempt
    if request.method == "POST":
        errors1 = User.objects.login_validator(request.POST)
        if len(errors1) > 0:
            for key, value in errors1.items():
                messages.error(request, value)
            return redirect('/')
        else:
            LoggedUser = User.objects.get(email=request.POST['logemail'])
            request.session['user'] = LoggedUser.id
            request.session['name'] = LoggedUser.first_name
            
            # request.session['id'] = LoggedUser.id
            return redirect('/dashboard')
    else:
        return redirect('/')
    
def logout(request):
    request.session.flush()
    print(request.session)
    return redirect('/')

def dashboard(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        "all_items": Item.objects.all(),
        "current_user": User.objects.get(id=request.session['user'])
    }
    return render(request, 'dashboard.html', context)