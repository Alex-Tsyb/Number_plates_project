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
            range(self.start_number, self.start_number + self.count_parking_place)
        )
        _ = [numbers_parking_place.remove(x) for x in self.excluded_numbers]
        return numbers_parking_place

    def get_free_parking_place(self):
        not_closed = Session.get_not_closed_sessions(place=self)
        # Check if not closed
        print(not_closed)
        return self.get_list_parking_place()
        # .remove(list_not_closed)

    def get_list_parking_place_with_description(self):
        pass


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

    def __str__(self):
        current_duration = self.calculate_duration()
        text_session_duration = "тривала" if self.end_time else "триває"
        return f"Паркувальна сесія '{self.parking_place}' номер місця {self.place_number} : {self.vehicle} з {self.start_time.strftime('%Y-%m-%d %H:%M')} {text_session_duration} {current_duration} годин"

    def get_not_closed_sessions(self, place: Place = None):
        if not place is None:
            return Session.objects.filter(end_time__isnull=True, parking_place=place)
        else:
            return Session.objects.filter(end_time__isnull=True)


# Модель для звітів паркувальних сесій
class Report(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to="reports/")

    def __str__(self):
        return f"Звіт для {self.vehicle} ({self.created_at})"


def generate_admin_statistics():
    # total_cars = Car.objects.count()
    # blacklisted_cars = Car.objects.filter(blacklisted=True).count()
    # total_parking_sessions = Car.objects.exclude(exit_time=None).count()
    # total_profit = sum(car.total_fee for car in Car.objects.exclude(total_fee=0))

    total_cars = 100
    blocked_cars = 1
    total_parking_sessions = 10
    total_profit = 50
    return {
        "total_cars": total_cars,
        "blocked_cars": blocked_cars,
        "total_parking_sessions": total_parking_sessions,
        "total_profit": total_profit,
    }
