from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Meal, CollabGroup

from django import forms
from django.forms.widgets import PasswordInput, TextInput, HiddenInput

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
        fields = '__all__'
        widgets = {'type': forms.HiddenInput(), 'date': forms.HiddenInput(), 'collab_group': forms.HiddenInput()}

class AddMemberForm(forms.ModelForm):
    # members = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter user email'}))
    
    class Meta:
        model = CollabGroup
        fields = '__all__'
