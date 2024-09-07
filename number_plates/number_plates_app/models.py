from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Додаємо аргумент related_name для уникнення конфліктів
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Унікальне ім'я для зв'язку груп
        blank=True,
        help_text='Групи, до яких належить цей користувач. Користувач отримає всі дозволи, надані кожній із груп.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Унікальне ім'я для зв'язку дозволів
        blank=True,
        help_text='Специфічні дозволи для цього користувача.',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username

class Car(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=15)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.license_plate
    
    # Метод для розрахунку суми за паркування
    def calculate_fee(self):
        if self.exit_time and self.entry_time:
            # Наприклад, $5 за годину паркування
            parking_duration = self.exit_time - self.entry_time
            hours_parked = parking_duration.total_seconds() // 3600
            self.total_fee = hours_parked * 5  # Наприклад, $5 за годину
            self.save()
