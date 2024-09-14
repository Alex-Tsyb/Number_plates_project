from django.db import models

# Create your models here.

class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    blocked = models.BooleanField(default=False)


# old code

# class Car(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     license_plate = models.CharField(max_length=15)
#     entry_time = models.DateTimeField(auto_now_add=True)
#     exit_time = models.DateTimeField(null=True, blank=True)
#     total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     blacklisted = models.BooleanField(default=False)


#     def __str__(self):
#         return self.license_plate
    
#     # Метод для розрахунку суми за паркування
#     def calculate_fee(self):
#         if self.exit_time and self.entry_time:
#             # Наприклад, $5 за годину паркування
#             parking_duration = self.exit_time - self.entry_time
#             hours_parked = parking_duration.total_seconds() // 3600
#             self.total_fee = hours_parked * 5  # Наприклад, $5 за годину
#             self.save()


# def generate_admin_statistics():
#     total_cars = Car.objects.count()
#     blacklisted_cars = Car.objects.filter(blacklisted=True).count()
#     total_parking_sessions = Car.objects.exclude(exit_time=None).count()
#     total_profit = sum(car.total_fee for car in Car.objects.exclude(total_fee=0))


#     return {
#         'total_cars': total_cars,
#         'blacklisted_cars': blacklisted_cars,
#         'total_parking_sessions': total_parking_sessions,
#         'total_profit': total_profit,
#     }

# Модель для чорного списку транспортних засобів
# class Blacklist(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     reason = models.TextField()

#     def __str__(self):
#         return f"{self.vehicle} в чорному списку"

