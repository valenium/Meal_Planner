from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

from django import forms
from django.forms.widgets import PasswordInput, TextInput

# Register user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2',]

class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=PasswordInput())
