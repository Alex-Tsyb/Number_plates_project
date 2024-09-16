from django.shortcuts import render, redirect

from .repository import get_places_info, generate_admin_statistics


def index(request):
    return render(request, "parking/index.html")


def rules(request):
    return render(request, "parking/rules.html")


def admin_dashboard(request):
    stats = generate_admin_statistics()

    context = {"stats": stats}
    return render(request, "parking/admin_dashboard.html", context)


def parking_plan(request):
    places_info = get_places_info()

    context = {"places_info": places_info}

    return render(request, "parking/parking_plan.html", context)
