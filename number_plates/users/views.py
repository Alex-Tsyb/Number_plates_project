from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm

def menu(request):
    return render(request, 'users/menu.html')

def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='number_plates_app:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.license_plate = form.cleaned_data['license_plate']
            user.save()
            return redirect(to='number_plates_app:index')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='number_plates_app:index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(to='number_plates_app:index')
            else:
                messages.error(request, 'Username or password didn\'t match')
        else:
            messages.error(request, 'Invalid form submission')
    
    else:
        form = LoginForm()

    return render(request, 'users/login.html', context={"form": form})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='number_plates_app:index')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your\
                        password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'
