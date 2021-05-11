from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    username = forms.CharField(label="Usuário")
    email = forms.CharField(label="Email")
    password1 = forms.CharField(label="Senha")
    password2 = forms.CharField(label="Repita sua senha")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha")
