from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2'
        ]

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email']