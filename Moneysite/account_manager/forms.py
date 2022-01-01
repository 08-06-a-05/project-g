from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Users

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control-with-text', 'aria-describedby': 'emailHelp', 'placeholder': "Email"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Повторите пароль'}))

    class Meta(UserCreationForm.Meta):
        model = Users
        fields = {
            'email',
            'username',
            'password1', 
            'password2'
        }   
