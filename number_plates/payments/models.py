from django.db import models

from django.contrib.auth.models import User

# Модель для обліку рахунку користувача
class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # зв'язок з користувачем
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # зв'язок з користувачем
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # сума транзакції
    transaction_type = models.CharField(max_length=10, choices=(('ADD', 'Add'), ('DEDUCT', 'Deduct')))  # тип транзакції
    created_at = models.DateTimeField(auto_now_add=True)  # час транзакції

    def __str__(self):
        return f'{self.user.username} - {self.transaction_type} {self.amount} on {self.created_at}'
    

# Модель для перевірки балансу користувача
class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # зв'язок з користувачем
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
