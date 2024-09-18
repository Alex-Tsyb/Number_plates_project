from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CarForm, UploadImageForRecognize

from .repository import predict_license_plate

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

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadImageForRecognize(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get("image")
            if uploaded_file:
                filename = uploaded_file.name

                detected_license_plate_img, plate_img, plate_text = predict_license_plate(uploaded_file, filename)

                form = CarForm(initial={"license_plate": plate_text})

                context = {}
                context["filename"] = filename
                context["detected_license_plate_img"] = detected_license_plate_img
                context["plate_img"] = plate_img
                context["predict_license_plate"] = plate_text
                context["form"] = form

                return render(request, 'cars/recognize.html', context)
            
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to ="cars:upload_file")
        
    else:
        form = UploadImageForRecognize()

    context = {}
    context["form"] = form

    return render(request, 'cars/upload_file.html', context)
