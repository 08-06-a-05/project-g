from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Users


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control-with-text', 'aria-describedby': 'emailHelp', 'placeholder': "Email",
               'id': 'email', 'autofocus': 'none'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя', 'id': 'name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Пароль', 'minlength': '8', 'id': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Повторите пароль', 'id': 'password_check'}))

    class Meta(UserCreationForm.Meta):
        model = Users
        fields = {
            'email',
            'username',
            'password1',
            'password2'
        }
