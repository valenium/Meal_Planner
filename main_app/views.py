from django.shortcuts import render, redirect

from django.http import HttpResponse

from . forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my-login")
    
    context = {'registerform':form}
    return render(request, 'authentication/register.html', context=context)

def my_login(request):
    form = LoginForm()

    if request.method =='POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            email = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect("dashboard")
        
    context = {'loginform':form}

    return render(request, 'authentication/my-login.html', context=context)

def user_logout(request):
    logout(request)

@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'dashboard.html')