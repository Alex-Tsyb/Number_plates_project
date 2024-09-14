from django.urls import path
from . import views

app_name = 'number_plates_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tarif/', views.tarif, name='tarif'),
    path('rules/', views.rules, name='rules'),
    path('contacts/', views.contacts, name='contacts'),
]
