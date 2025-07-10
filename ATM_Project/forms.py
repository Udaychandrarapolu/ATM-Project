from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    pin = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class DepositForm(forms.Form):
    amount = forms.DecimalField()

class WithdrawForm(forms.Form):
    amount = forms.DecimalField()
