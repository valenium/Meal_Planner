from django.shortcuts import render, redirect

from django.http import HttpResponse

from . forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from .models import 
# Create your views here.

# homepage
def home(request):
    return render(request, 'home.html')

# register new user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my-login")
    
    context = {'registerform':form}
    return render(request, 'authentication/register.html', context=context)

# login
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

# logout
def user_logout(request):
    logout(request)
    return redirect("home")

@login_required(login_url="my-login")
# dashboard to access groups
def dashboard(request):
    return render(request, 'dashboard.html')

# class UserUpdate(UpdateView):
#     model = 