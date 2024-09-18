from django.urls import path

from . import views

app_name = "cars"

urlpatterns = [
    path("add_car", views.create_vehicle, name="add_car"),
    path("upload_file", views.upload_file, name="upload_file"),
]