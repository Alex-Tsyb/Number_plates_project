from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserBalance, PaymentTransaction

# View для перевірки балансу користувача
@login_required
def check_balance(request):
    user_balance, created = UserBalance.objects.get_or_create(user=request.user)
    return render(request, 'payments/balance.html', {'balance': user_balance.balance})

# View для поповнення балансу
@login_required
def add_funds(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        user_balance, created = UserBalance.objects.get_or_create(user=request.user)
        user_balance.add_funds(amount)
        PaymentTransaction.objects.create(user=request.user, amount=amount, transaction_type='ADD')
        return redirect('check_balance')
    return render(request, 'payments/add_funds.html')

# View для історії транзакцій
@login_required
def transaction_history(request):
    transactions = PaymentTransaction.objects.filter(user=request.user)
    return render(request, 'payments/transaction_history.html', {'transactions': transactions})
