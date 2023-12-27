from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'balance_after_transaction', 'transaction_type', 'loan_approve']

    def save_model(self, request, obj, form, change):
        # Check if obj.account.balance and obj.amount are not None before performing addition
        if obj.account.balance is not None and obj.amount is not None:
            obj.account.balance += obj.amount
            obj.balance_after_transaction = obj.account.balance
            obj.account.save()

        super().save_model(request, obj, form, change)
