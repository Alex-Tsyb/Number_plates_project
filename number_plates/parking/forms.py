# from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Place, Session

from .repository import get_cars_for_choice, get_free_parking_places_for_choice


class SessionForm(forms.ModelForm):

    parking_place = forms.ModelChoiceField(
        queryset=Place.objects.all(),
        required=True,
    )
    place_number = forms.CharField(
        required=True,
    )
    vehicle = forms.ModelChoiceField(
        queryset=get_cars_for_choice(),
        required=True,
    )

    start_time = forms.DateTimeField(
        required=True,
    )
    end_time = forms.DateTimeField(
        required=False,
    )

    class Meta:
        model = Session
        fields = ["parking_place", "place_number", "vehicle", "start_time", "end_time"]


# old code
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2']

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email')

#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return cd['password2']
