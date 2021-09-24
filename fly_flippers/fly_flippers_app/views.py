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
    # gear = Item.objects.all()
    context = {
        "all_items": Item.objects.all(),
        "current_user": User.objects.get(id=request.session['user'])
    }
    return render(request, 'dashboard.html', context)

def new(request):
    if 'user' not in request.session:
        return redirect ('/')
    form = ItemForm()
    
    context = {
        "current_user": User.objects.get(id=request.session['user']),
        'form': form
    }
    return render(request, 'new.html', context)


def create(request):
    if 'user' not in request.session:
        return redirect('/')
    # errors = Item.objects.validateLengthGreaterThanTwo(request.POST) ##errors = Item.objects.basic_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect('items/new')
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()##saves user form inputs
            item.poster = User.objects.get(id=request.session['user'])##attaches who submitted the form to the poster field
            item.save()##saves it to db
            return redirect('/dashboard')
        else:
            print(form.errors)
            return render(request, 'new.html', {'form': form})
    return redirect('/dashboard')



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
    else:
        this_item = Item.objects.get(id=item_id)
        form = ItemForm(instance=this_item)
        context = {
            'current_item': this_item,
            'form': form
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

def favorite(request, item_id):
    if 'user' not in request.session:
        return redirect('/')
    item = Item.objects.get(id=item_id)
    item.favorite=True
    item.save()
    
    return redirect('/dashboard')

def unfavorite(request, item_id):
    if 'user' not in request.session:
        return redirect('/')
    item = Item.objects.get(id=item_id) ##id here represents simply a field in that model
    item.favorite=False
    item.save()
    
    return redirect('/dashboard')

def gallery(request):
    if 'user' not in request.session:
        return redirect('/')
    gallery = Item.objects.all()
    context = {
        'photos': gallery,
    }
    return render(request, 'gallery.html', context)