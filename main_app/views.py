from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponseRedirect

from . forms import CreateUserForm, LoginForm, MealForm, AddMemberForm, AddGroupForm, RemoveGroupForm, GroupUpdateForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.widgets import HiddenInput
from django.urls import reverse_lazy


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

    if request.method == 'POST':
        form = AddGroupForm(request.POST)
        if form.is_valid():
            group_id = form.cleaned_data['group_id']
            try:
                group = CollabGroup.objects.get(id=group_id)
                user.collab_groups.add(group)
                group.members.add(user)

                return redirect('/dashboard')
            
            except CollabGroup.DoesNotExist:
                form.add_error('group_id', 'This group does not exist.')
    else:
        form = AddGroupForm()
    
    return render(request, 'dashboard.html', { 'user': user, 'form': form })

# group index
def groups_index(request):
    user = request.user
    add_form = AddGroupForm()
    remove_form = RemoveGroupForm()

    if request.method == 'POST':
        if 'add' in request.POST.get('action',''):
            add_form = AddGroupForm(request.POST)
            remove_form = RemoveGroupForm()
            if add_form.is_valid():
                group_id = add_form.cleaned_data['group_id']
                try:
                    group = CollabGroup.objects.get(id=group_id)
                    user.collab_groups.add(group)
                    group.members.add(user)

                    return redirect('/dashboard')
            
                except CollabGroup.DoesNotExist:
                    add_form.add_error('group_id', 'This group does not exist.')
        
    
        elif 'remove' in request.POST.get('action',''):
            remove_form = RemoveGroupForm(request.POST)
            add_form = AddGroupForm()
            if remove_form.is_valid():
                groups = remove_form.cleaned_data['groups']
                for group in groups:
                    user.collab_groups.remove(group)
                return redirect('/groups')
        
        else:
            add_form = AddGroupForm()
            remove_form = RemoveGroupForm()

    return render(request, 'group/index.html', { 'user': user, 'add_form': add_form, 'remove_form': remove_form })

def group_leave(request, group_id):
    user = request.user

    if request.method == 'POST':
        try:
            group = CollabGroup.objects.get(id=group_id)
            user.collab_groups.remove(group)
        except CollabGroup.DoesNotExist:
            pass
    return redirect('group_index')

# group detail
def groups_detail(request, collabgroup_id):
    group = CollabGroup.objects.get(id=collabgroup_id)

    form = AddMemberForm()
    
    return render(request, 'group/detail.html', { 'group': group, 'form': form})

# Recipes index
def recipes_index(request, collabgroup_id):
    collab_group = get_object_or_404(CollabGroup, pk=collabgroup_id)
    recipes = Recipes.objects.filter(collab_group=collab_group).order_by('title')
    return render(request, 'group/recipe/index.html', { 'collab_group': collab_group, 'recipes': recipes})

def recipes_detail(request, collabgroup_id, recipe_id):
    recipe = get_object_or_404(Recipes, pk=recipe_id, collab_group_id=collabgroup_id)
    print(collabgroup_id)
    return render(request, 'group/recipe/detail.html', { 'recipe': recipe, 'collabgroup_id': collabgroup_id })

def meal_create(request):
    form = MealForm()

    if request.method == "POST":
        form = MealForm(request.POST)
        form.save()

    return render(request, 'group/meal/index.html', { 'meal_form': form })
    
# Meal calendar
def meal_calendar(request, collabgroup_id, year=datetime.now().year, week=None):
    # Calculating dates
    if week is None:
        week = datetime.now().isocalendar()[1]
        year = datetime.now().isocalendar()[0]

    collab_group = CollabGroup.objects.get(id=collabgroup_id)

    week = int(week)
    year = int(year)
    first_day_of_week = datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w").date()
    last_day_of_week = first_day_of_week + timedelta(days=6)

    prev_week = first_day_of_week - timedelta(weeks=1)
    next_week = first_day_of_week + timedelta(days=7)

    meals_for_week = Meal.objects.filter(
        date__range=[first_day_of_week, last_day_of_week],
        recipe__collab_group=collab_group,
    ).select_related('recipe').order_by('date', 'type')

    meals_by_day_type = defaultdict(lambda: {'B': None, 'L': None, 'D': None})
    for meal in meals_for_week:
        weekday = meal.date.weekday()
        meals_by_day_type[weekday][meal.type] = meal

    week_days = [first_day_of_week + timedelta(days=i) for i in range(7)]

    print(Recipes.objects.filter(collab_group__id=collabgroup_id).query)

    form = MealForm(collabgroup_id=collabgroup_id)
    # New meal form
    if request.method == "POST":
        form = MealForm(request.POST, collabgroup_id=collabgroup_id)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.collab_group = collab_group
            meal.save()
            return HttpResponseRedirect(request.path_info)
        else:
            form = MealForm(collabgroup_id=collabgroup_id)
            

    context = {
        'collab_group': collab_group,
        'meals_by_day_type': dict(meals_by_day_type),
        'week_days': week_days,
        'current_week': week,
        'current_year': year,
        'prev_week': prev_week.isocalendar()[1],
        'prev_year': prev_week.year,
        'next_week': next_week.isocalendar()[1],
        'next_year': next_week.year,
        'meal_form': form
    }
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
class GroupCreate(LoginRequiredMixin, CreateView):
    model = CollabGroup
    fields = ['name']

    def form_valid(self, form):
        member = self.request.user
        print(member.id)
        # form.members.set(member)
        group = form.save()

        group.members.add(member)
        member.collab_groups.add(group)
        return super().form_valid(form)

# Group delete
class GroupDelete(DeleteView):
    model = CollabGroup
    success_url = '/dashboard'

# Group update
class GroupUpdate(UpdateView):
    model = CollabGroup
    form_class = GroupUpdateForm
    template_name = 'main_app/collabgroup_update.html'
    success_url = reverse_lazy('group_detail') 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if 'remove_user' in request.POST:
            user_id = request.POST.get('remove_user')
            user = get_object_or_404(CustomUser, id=user_id)
            self.object.members.remove(user)
            return self.form_valid(form)
        
        else:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.members.all()
        return context

# Recipe edit
class RecipeUpdate(UpdateView):
    model = Recipes
    fields = ['title', 'url', 'ingredients', 'instructions']

# Recipe create
class RecipeCreate(CreateView):
    model = Recipes
    fields = ['title', 'url', 'ingredients', 'instructions']

    def form_valid(self, form):
        collab_group = get_object_or_404(CollabGroup, pk=self.kwargs['collabgroup_id'])
        form.instance.collab_group = collab_group
        return super().form_valid(form)

# Recipe delete
class RecipeDelete(DeleteView):
    model = Recipes

    def get_success_url(self):
        group_id = self.kwargs.get('collabgroup_id')
        return reverse_lazy('recipes_index', kwargs={'collabgroup_id': group_id})

class MealUpdate(UpdateView):
    model = Meal
    fields = ['recipe']

    def get_form(self, form_class=None):
        form = super(MealUpdate, self).get_form(form_class)
        meal = self.get_object()
        form.fields['recipe'].queryset = Recipes.objects.filter(collab_group=meal.collab_group)
        return form

class MealDelete(DeleteView):
    model = Meal

    def get_success_url(self):
        return self.object.get_absolute_url()
