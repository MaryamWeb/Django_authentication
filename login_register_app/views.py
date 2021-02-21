from django.shortcuts import render, redirect 
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        errors = User.objects.validateRegister(request.POST)
        if len( errors) > 0:  
            for key, value in errors.items():  
                messages.error(request, value)
            return redirect('/')
        else:  #create user and set sessions if no error occurred
            password=request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
            user = User.objects.create(first_name=request.POST['first_name'], email=request.POST['email'].lower(), password=pw_hash)
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
    return redirect('/')

def login(request):
    if request.method == 'POST':
        logged_user = User.objects.get(email=request.POST['email'].lower())
        request.session['user_id'] = logged_user.id
        request.session['first_name'] = logged_user.first_name
    return redirect('/')