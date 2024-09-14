from django.contrib import admin
from .models import PaymentTransaction, UserBalance


admin.site.register(PaymentTransaction)
admin.site.register(UserBalance)
