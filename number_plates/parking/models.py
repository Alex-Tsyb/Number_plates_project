from typing import Iterable
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

from cars.models import Car
from parking_rates.models import ParkingRate
from payments.models import PaymentTransaction


class Place(models.Model):
    description = models.CharField(max_length=255)
    count_parking_place = models.IntegerField()
    start_number = models.IntegerField()
    excluded_numbers = ArrayField(models.IntegerField(), default=list, blank=True)

    def __str__(self):
        # print(self.get_free_parking_plase())
        return f"{self.description} for {self.count_parking_place} places"

    def get_list_numbers_parking_place(self):
        numbers_parking_place = list(
            range(
                self.start_number,
                self.start_number
                + self.count_parking_place
                + len(self.excluded_numbers),
            )
        )
        _ = [numbers_parking_place.remove(x) for x in self.excluded_numbers]
        return numbers_parking_place


# Модель для паркувальних сесій
class Session(models.Model):
    parking_place = models.ForeignKey(Place, on_delete=models.CASCADE)
    place_number = models.IntegerField()
    vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(
        null=True, blank=True
    )  # Якщо не завершено, поле порожнє
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment = models.ManyToManyField(PaymentTransaction, blank=True)

    def __str__(self):
        current_duration = self.calculate_duration()
        text_session_duration = "тривала" if self.end_time else "триває"
        return f"Паркувальна сесія '{self.parking_place}' номер місця {self.place_number} : {self.vehicle} з {self.start_time.strftime('%Y-%m-%d %H:%M')} {text_session_duration} {current_duration} годин"

    def calculate_duration(self):
        duration = 0
        if self.end_time is None:
            duration = timezone.now() - self.start_time
        else:
            duration = self.end_time - self.start_time

        # Тривалість у годинах
        return round(duration.total_seconds() / 3600, 2)

    def calculate_cost(self):
        if self.end_time:
            duration = self.calculate_duration()
            parking_rate = (
                ParkingRate.objects.first()
            )  # Припускаємо, що є лише один тариф
            return min(duration * parking_rate.rate_per_hour, parking_rate.max_limit)
        return 0


# Модель для звітів паркувальних сесій
class Report(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to="reports/")

    def __str__(self):
        return f"Звіт для {self.vehicle} ({self.created_at})"
