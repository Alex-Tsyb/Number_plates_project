from django.urls import path
from . import views

from parking_rates import views as parking_rates_views
from cars import views as cars_views

app_name = 'parking'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tarifs/', parking_rates_views.index, name='tarif'),
    path('rules/', views.rules, name='rules'),
    path('parking_plan/', views.parking_plan, name='parking_plan'), 

    # path('cars/', cars_views.index, name='cars'),
    # path('cars/<int:pk>/', cars_views.index, name='cars'),
    path('add_car/', cars_views.create_vehicle, name='add_car'),

    path('parking_session/', views.parking_session, name='parking_session'),
    path('parking_session/<int:pk>/', views.parking_session, name='parking_session_edit'),

    path('parking_session_dialog/', views.parking_session_dialog, name='parking_session_dialog'),
    path('parking_session_dialog/<int:pk>/', views.parking_session_dialog, name='parking_session_dialog_edit'),
]

