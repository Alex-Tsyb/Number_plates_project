from django.db import models


# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Модель користувача
class User(AbstractUser):
    USER_ROLES = [
        ('admin', 'Адміністратор'),
        ('user', 'Користувач'),
    ]
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')

    def __str__(self):
        return self.username


# Модель для зберігання інформації про автомобільні номерні знаки
class Vehicle(models.Model):
    license_plate = models.CharField(max_length=15, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.license_plate


# Модель для тарифів на паркування
class ParkingRate(models.Model):
    rate_per_hour = models.DecimalField(max_digits=6, decimal_places=2)  # Вартість паркування за годину
    max_limit = models.DecimalField(max_digits=8, decimal_places=2)  # Максимальний ліміт вартості

    def __str__(self):
        return f"{self.rate_per_hour} грн/год"


# Модель для паркувальних сесій
class ParkingSession(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)  # Якщо не завершено, поле порожнє
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def calculate_duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 3600  # Тривалість у годинах
        return 0

    def calculate_cost(self):
        if self.end_time:
            duration = self.calculate_duration()
            parking_rate = ParkingRate.objects.first()  # Припускаємо, що є лише один тариф
            return min(duration * parking_rate.rate_per_hour, parking_rate.max_limit)
        return 0

    def __str__(self):
        return f"Паркувальна сесія {self.vehicle} з {self.start_time}"


# Модель для чорного списку транспортних засобів
class Blacklist(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f"{self.vehicle} у чорному списку"


# Модель для звітів паркувальних сесій
class ParkingReport(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    session = models.ForeignKey(ParkingSession, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"Звіт для {self.vehicle} ({self.created_at})"
