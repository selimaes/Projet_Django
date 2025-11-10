from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "affiliation", "nationality", "password1", "password2"]
        widget = {
            "email": forms.EmailInput(),
            "password1": forms.PasswordInput(),
        }
