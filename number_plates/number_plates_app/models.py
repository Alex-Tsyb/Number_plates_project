from django.db import models

class ParkingRate(models.Model):
    rate_per_hour = models.DecimalField(max_digits=6, decimal_places=2)  # Вартість паркування за годину
    max_limit = models.DecimalField(max_digits=8, decimal_places=2)  # Максимальний ліміт вартості

    def __str__(self):
        return f"{self.rate_per_hour} грн/год"