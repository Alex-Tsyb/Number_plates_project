from django.db import models
from django.utils import timezone

from cars.models import Car
from parking_rates.models import ParkingRate


# Модель для паркувальних сесій
class ParkingSession(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
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
    

# Модель для звітів паркувальних сесій
class ParkingReport(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    session = models.ForeignKey(ParkingSession, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"Звіт для {self.vehicle} ({self.created_at})"
    


