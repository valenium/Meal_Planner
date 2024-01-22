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

class AddGroupForm(forms.Form):
    group_id = forms.IntegerField(label='Group ID')
    action = forms.CharField(max_length=10, widget=forms.HiddenInput(), initial='add')


    def clean_group_id(self):
        group_id = self.cleaned_data['group_id']

        if not CollabGroup.objects.filter(id=group_id).exists():
            raise forms.ValidationError('Collab Group with this ID does not exist.')
        return group_id
    
class RemoveGroupForm(forms.Form):
    group = forms.ModelMultipleChoiceField(queryset=CollabGroup.objects.none(), widget=forms.CheckboxSelectMultiple, required=False)
    action = forms.CharField(max_length=10, widget=forms.HiddenInput(), initial='remove')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            print(user.collab_groups.all())
            self.fields['groups_to_remove'].queryset = user.collab_groups.all()


class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = CollabGroup
        fields = ['name']