from django.urls import path
from . import views

app_name = "tarif"

urlpatterns = [
    path("", views.index, name="index"),
]