from django.urls import path
from .views import WithdrawMoneyView,DepositMoneyView,TransactionReportView

urlpatterns = [
    path('withdraw/',WithdrawMoneyView.as_view(),name= 'withdraw_money'),
    path('deposit/',DepositMoneyView.as_view(),name= 'deposit_money'),
    path("report/", TransactionReportView.as_view(), name="transaction_report"),


]
