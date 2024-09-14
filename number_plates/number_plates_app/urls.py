from django.urls import path
from . import views

from parking_rates import views as parking_rates_views

app_name = 'number_plates_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tarifs/', parking_rates_views.index, name='tarif'),
    path('rules/', views.rules, name='rules'),
]
