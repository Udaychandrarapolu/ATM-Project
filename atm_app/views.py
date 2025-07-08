from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, DepositForm, WithdrawForm
from .models import Account, Transaction

# --------------------------
# User Registration View
# --------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Secure password
            user.save()

            # Create Account with PIN and 0 balance
            Account.objects.create(user=user, pin=form.cleaned_data['pin'])
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'atm_app/register.html', {'form': form})

# --------------------------
# User Login View with PIN
# --------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        pin = request.POST['pin']

        user = authenticate(request, username=username, password=password)
        if user:
            try:
                account = Account.objects.get(user=user)
                if account.pin == pin:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'atm_app/login.html', {'error': 'Invalid PIN'})
            except Account.DoesNotExist:
                return render(request, 'atm_app/login.html', {'error': 'Account not found'})
        else:
            return render(request, 'atm_app/login.html', {'error': 'Invalid credentials'})

    return render(request, 'atm_app/login.html')

# --------------------------
# Dashboard View (After Login)
# --------------------------
@login_required
def dashboard_view(request):
    account = Account.objects.get(user=request.user)
    return render(request, 'atm_app/dashboard.html', {'account': account})

# --------------------------
# Deposit Money View
# --------------------------
@login_required
def deposit_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            account.balance += amount
            account.save()

            Transaction.objects.create(account=account, type='Deposit', amount=amount)
            return redirect('dashboard')
    else:
        form = DepositForm()
    return render(request, 'atm_app/deposit.html', {'form': form})

# --------------------------
# Withdraw Money View
# --------------------------
@login_required
def withdraw_view(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)

            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, type='Withdraw', amount=amount)
                return redirect('dashboard')
            else:
                return render(request, 'atm_app/withdraw.html', {'form': form, 'error': 'Insufficient funds'})
    else:
        form = WithdrawForm()
    return render(request, 'atm_app/withdraw.html', {'form': form})

# --------------------------
# Transaction History View
# --------------------------
@login_required
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')
    return render(request, 'atm_app/history.html', {'transactions': transactions})

# --------------------------
# Logout View
# --------------------------
def logout_view(request):
    logout(request)
    return redirect('login')
