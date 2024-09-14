from django.contrib import admin
from .models import ParkingSession, ParkingReport

admin.site.register(ParkingSession)
admin.site.register(ParkingReport)
