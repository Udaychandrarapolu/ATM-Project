from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages

# ✅ Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'ATM_Project/login.html')


# ✅ Register View (fixes your error)
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Username already exists.')
    return render(request, 'ATM_Project/register.html')


# ✅ Dashboard View
@login_required
def dashboard_view(request):
    return render(request, 'ATM_Project/dashboard.html')


# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# ✅ Deposit View
@login_required
def deposit_view(request):
    if request.method == 'POST':
        # handle deposit logic here
        messages.success(request, 'Deposit successful.')
        return redirect('dashboard')
    return render(request, 'ATM_Project/deposit.html')


# ✅ Withdraw View
@login_required
def withdraw_view(request):
    if request.method == 'POST':
        # handle withdraw logic here
        messages.success(request, 'Withdrawal successful.')
        return redirect('dashboard')
    return render(request, 'ATM_Project/withdraw.html')


# ✅ Transaction History View
@login_required
def transaction_history(request):
    # fetch transactions from DB
    return render(request, 'ATM_Project/transactions.html')
