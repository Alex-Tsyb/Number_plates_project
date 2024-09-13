from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    license_plate = models.CharField(max_length=20, blank=True, null=True)

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
    blacklisted = models.BooleanField(default=False)


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


def generate_admin_statistics():
    total_cars = Car.objects.count()
    blacklisted_cars = Car.objects.filter(blacklisted=True).count()
    total_parking_sessions = Car.objects.exclude(exit_time=None).count()
    total_profit = sum(car.total_fee for car in Car.objects.exclude(total_fee=0))


    return {
        'total_cars': total_cars,
        'blacklisted_cars': blacklisted_cars,
        'total_parking_sessions': total_parking_sessions,
        'total_profit': total_profit,
    }

# Модель для тарифів на паркування
class ParkingRate(models.Model):
    rate_per_hour = models.DecimalField(max_digits=6, decimal_places=2)  # Вартість паркування за годину
    max_limit = models.DecimalField(max_digits=8, decimal_places=2)  # Максимальний ліміт вартості

    def __str__(self):
        return f"{self.rate_per_hour} грн/год"


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


# Модель для чорного списку транспортних засобів
class Blacklist(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f"{self.vehicle} в чорному списку"


# Модель для звітів паркувальних сесій
class ParkingReport(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    session = models.ForeignKey(ParkingSession, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"Звіт для {self.vehicle} ({self.created_at})"
    
# Модель для перевірки балансу користувача
class UserBalance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # зв'язок з користувачем
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # баланс користувача

    def __str__(self):
        return f'{self.user.username} - Balance: {self.balance}'

    # Метод для додавання коштів на баланс
    def add_funds(self, amount):
        self.balance += amount
        self.save()

    # Метод для зняття коштів
    def deduct_funds(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False
    
# Модель для зберігання транзакцій
class PaymentTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # зв'язок з користувачем
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # сума транзакції
    transaction_type = models.CharField(max_length=10, choices=(('ADD', 'Add'), ('DEDUCT', 'Deduct')))  # тип транзакції
    created_at = models.DateTimeField(auto_now_add=True)  # час транзакції

    def __str__(self):
        return f'{self.user.username} - {self.transaction_type} {self.amount} on {self.created_at}'
