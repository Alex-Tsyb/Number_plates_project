from django.test import TestCase
from django.contrib.auth.models import User
from payments.models import Account, Transaction

class AccountTests(TestCase):
    def setUp(self):
        # Створюємо тестового користувача
        self.user = User.objects.create_user(username='testuser', password='password')
        # Створюємо аккаунт для користувача
        self.account = Account.objects.create(user=self.user, balance=100)

    def test_check_balance(self):
        # Перевіряємо, чи баланс користувача правильно отримується
        self.assertEqual(self.account.balance, 100)

class DepositTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.account = Account.objects.create(user=self.user, balance=100)

    def test_deposit(self):
        # Поповнюємо баланс на 50
        self.account.deposit(50)
        # Перевіряємо, чи баланс збільшився на 50
        self.assertEqual(self.account.balance, 150)

        # Перевіряємо, чи була створена транзакція
        transaction = Transaction.objects.filter(account=self.account).first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.amount, 50)
        self.assertEqual(transaction.transaction_type, 'deposit')


class TransactionHistoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.account = Account.objects.create(user=self.user, balance=100)

    def test_transaction_history(self):
        # Створюємо кілька транзакцій
        self.account.deposit(50)
        self.account.withdraw(20)

        # Отримуємо історію транзакцій
        transactions = Transaction.objects.filter(account=self.account).order_by('-timestamp')

        # Перевіряємо, що транзакцій дві
        self.assertEqual(transactions.count(), 2)

        # Перевіряємо деталі першої транзакції
        first_transaction = transactions[0]
        self.assertEqual(first_transaction.amount, 20)
        self.assertEqual(first_transaction.transaction_type, 'withdraw')

        # Перевіряємо деталі другої транзакції
        second_transaction = transactions[1]
        self.assertEqual(second_transaction.amount, 50)
        self.assertEqual(second_transaction.transaction_type, 'deposit')
