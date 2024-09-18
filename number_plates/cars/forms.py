from django import forms

from .models import Car

class CarForm(forms.ModelForm):
    
    class Meta:
        model = Car
        fields = ['license_plate', 'blocked']


class UploadImageForRecognize(forms.Form):
    image = forms.FileField()

    # photo = forms.ImageField(
    #     widget=forms.FileInput(
    #         attrs={
    #             "class": "form-control",
    #             "title": "Upload photo of car",
    #         }  # ,
    #     ),
    # )