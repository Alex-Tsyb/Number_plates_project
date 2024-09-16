from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CarForm

@login_required
def create_vehicle(request):
    
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="parking:index")
    else:
        form = CarForm()

    context = {}
    context["form"] = form

    return render(request, "cars/create_car.html", context)

