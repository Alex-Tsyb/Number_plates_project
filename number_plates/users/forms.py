from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from number_plates_app.models import CustomUser

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())

    email = forms.CharField(max_length=254,
                            required=True,
                            widget=forms.EmailInput())

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())
    license_plate = forms.CharField(max_length=20,
                                    required=True, 
                                    widget=forms.TextInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'license_plate']


class LoginForm(AuthenticationForm):

    username = forms.CharField(max_length=100, widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
