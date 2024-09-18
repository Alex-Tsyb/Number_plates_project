from django.contrib import admin
from .models import PaymentTransaction, UserBalance


@admin.register(PaymentTransaction)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "transaction_type", "created_at"]
    list_filter = ["created_at"]


admin.site.register(UserBalance)
