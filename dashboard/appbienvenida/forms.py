
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import fields
from django.db.models.base import Model
from django.forms.models import ModelForm
from .models import Archivo


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='Nombre', max_length=140, required=True)
    last_name = forms.CharField(label='Apellidos', max_length=140, required=False)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repite Contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

'''
class RegistroForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',

        ]
        labels = {
            'username':'nombre de usuario',
            'first_name':'nombre',
            'last_name':'apellidos',
            'email':'correo electrónico',
            'password1': 'contraseña',
            'password2': 'confirmar contraseña',

        }
'''

'''
class Formulario(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'user', 
            'email',
            #'message',

        ]
        labels = {
            'user':'nombre completo',
            'email':'correo electrónico',
            #'message':'mensaje',

        }
'''

'''
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model: User
        fields = [ 'username', "first_name", "last_name", "email", "password1", "passwoes2"]


    class Meta:
        model = User
        fields = [
            'username', 
            'first_name',
            'last_name',
            'email',
            'password',

        ]
        labels = {
            'username':'nombre de usuario',
            'first_name':'nombre',
            'last_name':'apellidos',
            'email':'correo electrónico',
            'password': 'contraseña',
        }


'''