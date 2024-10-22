from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_htmx.http import HttpResponseClientRefresh

from .repository import (
    get_session_by_id,
    get_places_info,
    generate_admin_statistics,
    get_data_session_by_id_for_form,
    get_data_for_new_session_for_form,
)
from .forms import SessionForm


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


@login_required
def parking_session(request, pk: int = None):

    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="parking:index")
    else:
        if not pk is None:
            object_session = get_data_session_by_id_for_form(pk)
            form = SessionForm(initial=object_session)
        else:
            form = SessionForm()

    context = {}
    context["type"] = "create" if not pk else "edit"
    context["form"] = form

    return render(request, "parking/parking_session.html", context)


@login_required
def parking_session_dialog(request, pk=None):

    if request.method == "POST":
        if not request.POST["modal-session_id"] == "":
            updated_session = get_session_by_id(int(request.POST["modal-session_id"]))
            form = SessionForm(data=request.POST, instance=updated_session, prefix="modal")
        else:
            form = SessionForm(data=request.POST, prefix="modal")
        if form.is_valid():
            form.save()
            return HttpResponseClientRefresh()

    else:
        if not pk is None:
            object_session = get_data_session_by_id_for_form(pk)
            form = SessionForm(initial=object_session, prefix="modal")
        else:
            object_new_session = get_data_for_new_session_for_form(request.GET)
            form = SessionForm(initial=object_new_session, prefix="modal")

    context = {}
    context["type"] = "create" if not pk else "edit"
    context["form"] = form

    return render(request, "parking/parking_session_dialog.html", context)
