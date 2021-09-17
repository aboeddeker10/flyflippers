from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
from .forms import ItemForm

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

def create(request):
    if 'user' not in request.session:
        return redirect('/')
    errors = Item.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('items/new')
    else:
        print(request.POST)
        c = Item.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price'],
            condition=request.POST['condition'],
            location=request.POST['location'],
            poster=User.objects.get(id=request.session["user"]),
        )
    return redirect('/dashboard')

def new(request):
    if 'user' not in request.session:
        return redirect ('/')
    form = ItemForm()
    
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        "current_user": User.objects.get(id=request.session['user']),
        'form': form
    }
    return render(request, 'new.html', context)

def details(request, item_id):
    if 'user' not in request.session:
        return redirect ('/')
    item_details = Item.objects.get(id=item_id)
    context = {
        'current_item': item_details,
        'current_user': User.objects.get(id=request.session['user'])
    }
    return render(request, 'item.html', context)

def edit(request, item_id):
    if 'user' not in request.session:
        return redirect('/')
    this_item = Item.objects.get(id=item_id)
    context = {
        'current_item': this_item
    }
    return render(request, 'edit.html', context)

def update(request, item_id):
    if 'user' not in request.session:
        return redirect('/')
    errors = Item.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/items/edit/{item_id}')
    else:
        # update it!
        to_update = Item.objects.get(id=item_id)
    # update each field
        to_update.name = request.POST['name']
        to_update.description = request.POST['description']
        to_update.price = request.POST['price']
        to_update.condition = request.POST['condition']
        to_update.location = request.POST['location']
        to_update.image = request.POST['image']
        to_update.save()

        return redirect('/dashboard')

def delete(request, item_id):
    if 'user' not in request.session:
        return redirect('/')
    # if request.method == "POST"
    # (id=request.POST['show_id'])  ##this helps validate so someone can't paste a user id into address bar
    c = Item.objects.get(id=item_id)
    c.delete()
    return redirect('/dashboard')