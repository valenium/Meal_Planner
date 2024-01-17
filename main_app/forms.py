from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Meal

from django import forms
from django.forms.widgets import PasswordInput, TextInput

# Register user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2',]

class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=PasswordInput())

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['type', 'recipe', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }