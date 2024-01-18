from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

from . forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import calendar
from datetime import datetime, timedelta
from collections import defaultdict

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
    
# Meal calendar
def meal_calendar(request, collabgroup_id, year=datetime.now().year, week=None):
    if week is None:
        week = datetime.now().isocalendar()[1]
        year = datetime.now().isocalendar()[0]

    collab_group = get_object_or_404(CollabGroup, pk=collabgroup_id)

    week = int(week)
    year = int(year)
    first_day_of_week = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w").date()
    last_day_of_week = first_day_of_week + timedelta(days=6)
    print(f'week {week}')
    print(datetime.now().isocalendar())
    print(f'first day of week {first_day_of_week} ')

    prev_week = first_day_of_week - timedelta(weeks=1)
    next_week = first_day_of_week + timedelta(days=7)

    print(f'next week {next_week} {next_week.year}')
    print(f'prev week {prev_week} {prev_week.year}')

    meals_for_week = Meal.objects.filter(
        date__range=[first_day_of_week, last_day_of_week],
        # collab_group=collab_group
        recipe__collab_group=collab_group,
    ).select_related('recipe').order_by('date', 'type')

    meals_by_day_type = defaultdict(lambda: {'B': None, 'L': None, 'D': None})
    for meal in meals_for_week:
        weekday = meal.date.weekday()
        meals_by_day_type[weekday][meal.type] = meal

    week_days = [first_day_of_week + timedelta(days=i) for i in range(7)]
    # next_week_start = last_day_of_week + timedelta(days=1)

    # next_week = next_week_start.isocalendar()[1]
    # next_year = next_week_start.year

    context = {
        'collab_group': collab_group,
        'meals_by_day_type': dict(meals_by_day_type),
        'week_days': week_days,
        'current_week': week,
        'current_year': year,
        'prev_week': prev_week.isocalendar()[1],
        'prev_year': prev_week.year,
        'next_week': next_week.isocalendar()[1],
        'next_year': next_week.year
    }
    print(f'{next_week} {next_week.year}')
    return render(request, 'group/meal/index.html', context)

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

# Group update
class GroupUpdate(UpdateView):
    model = CollabGroup
    fields = ['name', 'members']

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