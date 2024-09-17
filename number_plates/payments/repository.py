from django.db.models import Sum, Q
from .models import PaymentTransaction


def get_user_balance(user):
    all_transactions = PaymentTransaction.objects.filter(user=user)
    user_balance = all_transactions.aggregate(
        add_sum=Sum("amount", filter=Q(transaction_type="ADD"), default=0),
        deduct_sum=Sum("amount", filter=Q(transaction_type="DEDUCT"), default=0),
    )
    return float(user_balance["add_sum"] - user_balance["deduct_sum"])


def get_user_transactions(user, limit=5):
    return PaymentTransaction.objects.filter(user=user).order_by("-created_at")[:limit]
