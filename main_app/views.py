from django.shortcuts import render, redirect

from django.http import HttpResponse

from . forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .models import CustomUser, CollabGroup, Recipes, Meal
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
    
    return render(request, 'authentication/register.html', { 'registerform': form })

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

    return render(request, 'authentication/my-login.html', {'loginform':form})

# logout
def user_logout(request):
    logout(request)
    return redirect("home")

# dashboard to access groups
@login_required(login_url="my-login")
def dashboard(request):
    user = request.user
    print(user.first_name)
    # print(user.collab_group)
    # user_data = CustomUser.objects.filter(user=request.id)
    return render(request, 'dashboard.html', { 'user': user })

# group detail
def groups_detail(request, collabgroup_id):
    group = CollabGroup.objects.get(id=collabgroup_id)
    return render(request, 'group/detail.html', { 'group': group })

# Recipes index
# def recipe_index(request):
    
# User edit
class UserUpdate(UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name']

# User delete
class UserDelete(DeleteView):
    model = CustomUser
    success_url = '/'

# Group create
class GroupCreate(CreateView):
    model = CollabGroup
    fields = '__all__'

# Group delete
class GroupDelete(DeleteView):
    model = CollabGroup
    success_url = '/dashboard'

# Recipe edit
class RecipeUpdate(UpdateView):
    model = Recipes
    fields = ['title', 'url', 'ingredients', 'instructions']

# Recipe create
class RecipeCreate(CreateView):
    model = Recipes
    fields = '__all__'

# Recipe delete
class RecipeDelete(DeleteView):
    model = Recipes
    success_url = '/groups/recipes'