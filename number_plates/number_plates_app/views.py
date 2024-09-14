from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import Car, CustomUser, generate_admin_statistics

def contacts(request):
    return render(request, 'number_plates_app/contacts.html')

def index(request):
    return render(request, 'number_plates_app/index.html')

def tarif(request):
    return render(request, 'number_plates_app/tarif.html')

def rules(request):
    return render(request, 'number_plates_app/rules.html')

def user_parking_info(request):
    user_cars = Car.objects.filter(user=request.user)
    return render(request, 'user_parking_info.html', {'user_cars': user_cars})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()

            if not CustomUser.objects.filter(is_superuser=True).exists():
                new_user.is_superuser = True
                new_user.is_staff = True
                new_user.save()

            login(request, new_user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'number_plates_app/register.html', {'form': form})

def admin_dashboard(request):
    stats = generate_admin_statistics()
    return render(request, 'admin_dashboard.html', {'stats': stats})