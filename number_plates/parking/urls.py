from django.urls import include, path
from . import views

app_name = 'parking'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('rules/', views.rules, name='rules'),
    path('parking_plan/', views.parking_plan, name='parking_plan'), 

    path('parking_session/', views.parking_session, name='parking_session'),
    path('parking_session/<int:pk>/', views.parking_session, name='parking_session_edit'),

    path('parking_session_dialog/', views.parking_session_dialog, name='parking_session_dialog'),
    path('parking_session_dialog/<int:pk>/', views.parking_session_dialog, name='parking_session_dialog_edit'),
]

