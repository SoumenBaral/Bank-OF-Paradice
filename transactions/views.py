from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect,render
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from transactions.constant import DEPOSIT, TRANSFER, WITHDRAWAL,LOAN, LOAN_PAID
from datetime import datetime
from django.db.models import Sum
from transactions.models import Transaction
from transactions.forms import (DepositForm,WithdrawForm, LoanRequestForm,)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from accounts.models import UserBankAccount
from decimal import Decimal
from accounts.models import isBankCraft


def send_Mail(user,amount,mail_subject,template):
        message= render_to_string(template, {
                "user": user,
                "amount": amount,
            })
        send_email =EmailMultiAlternatives(mail_subject,"", to=[user.email])
        send_email.attach_alternative(message,'text/html')
        send_email.send()




class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs  = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        
        })
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        context.update({
            'title':self.title
        })
        return context




class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Mony'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial
    
    def form_valid(self, form):
        if isBankCraft.objects.filter(Is_Bank_Craft=True).exists():
            messages.success(self.request, 'Your Bank is Bankrupt You can not Withdraw')
            

        else:
            amount = form.cleaned_data.get('amount')
            self.request.user.account.balance -= amount
            self.request.user.account.save(update_fields=['balance'])
            messages.success(self.request, f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account')
            send_Mail(self.request.user,amount,'Withdrawal Message','transactions/withdrawal_email.html')
        return super().form_valid(form)

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        account.balance += amount 
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

       
        send_Mail(self.request.user,amount,'Deposit Message','transactions/deposit_email.html')
        

        return super().form_valid(form)

class  LoanRequestView(TransactionCreateMixin):
    form_class =  LoanRequestForm
    title = 'Request For Loan'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transaction.objects.filter( account=self.request.user.account,transaction_type=3,loan_approve=True).count()
        if current_loan_count >= 3:
            return HttpResponse("You have cross the loan limits")
        messages.success(
            self.request,
            f'Loan request for {"{:,.2f}".format(float(amount))}$ submitted successfully'
        )
        send_Mail(self.request.user,amount,'Loan Request','transactions/loan_email.html')
        return super().form_valid(form)

class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0 # filter korar pore ba age amar total balance ke show korbe
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct() # unique queryset hote hobe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context


class  PayLoanView(LoginRequiredMixin, View):
    def get(self,request,loan_id):
        loan = get_object_or_404(Transaction,id = loan_id)
        print(loan)

        if loan.loan_approve:
            user_account = loan.account

            if user_account.balance is not None and loan.amount < user_account.balance:
                user_account.balance -=loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('loan_list')
            else:
                messages.error(self.request,f"Loan amount is greater then available balance ")

        return redirect('loan_list')

class LoanListView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'transactions/loan_request.html'
    context_object_name = 'loans' # loan list ta ei loans context er moddhe thakbe
    
    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transaction.objects.filter(account=user_account,transaction_type=3)
        print(queryset)
        return queryset
    

class TransferView(LoginRequiredMixin,View):
    template_name = 'transactions/transfer.html'

   
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self,request,*args, **kwargs):
        sender_account = self.request.user.account
        recipient_username = request.POST.get('recipient_username')
        amount = request.POST.get('amount')
        
    
        try:
            recipient_account = UserBankAccount.objects.get(user__username=recipient_username)
        except UserBankAccount.DoesNotExist:
            messages.warning(self.request, f'Recipient account not found')
            return render(request, self.template_name)
        
        if sender_account.balance >= Decimal(amount) > 0:
            sender_account.balance -= Decimal(amount)
            recipient_account.balance += Decimal(amount)
            messages.success(self.request, f'Successfully Transfer {"{:,.2f}".format(float(amount))}$ from your account')
            sender_account.save()
            recipient_account.save()

            return redirect('transfer_money')
        else:
            messages.warning(self.request, f'Insufficient funds')
            return render(request, self.template_name)


