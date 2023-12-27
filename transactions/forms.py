from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList 
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class meta :
        model = Transaction
        fields = ['amount','transaction_type']

    def __init__(self,*args, **kwargs):
        self.user_account = kwargs.pop('account') 
        # We get the current user Account 
        super().__init__(*args, **kwargs)
        # It calls the constructor of the parent class with the specified arguments and keyword arguments.
        self.fields['transaction_type'].disabled = True
        # This field will be disable 
        self.fields['transaction_type'].widget = forms.HiddenInput()
        # It will be hide from the user 

        def save(self, commit=True):
            self.instance.account = self.user_account
            self.instance.balance_after_transaction = self.account.balance
            return super().save()

class DepositForm(TransactionForm):
    def clean_amount(self):
        # we are gonna filter Amount field 
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        # we get the amount form the user fill up from 
        if amount<min_deposit_amount: 
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount}'
            )
        return amount

class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account = self.user_account
        min_withdraw_amount = 500
        max_withdraw_amount = 200000
        balance = account.balance 
        amount = self.cleaned_data.get['amount']

        if amount <min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount>balance:
            raise forms.ValidationError(
                 f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )
        
        return amount