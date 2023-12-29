from django.urls import path
from .views import TransferView, WithdrawMoneyView,DepositMoneyView,TransactionReportView,LoanRequestView,LoanListView,PayLoanView

urlpatterns = [
    path('withdraw/',WithdrawMoneyView.as_view(),name= 'withdraw_money'),
    path('deposit/',DepositMoneyView.as_view(),name= 'deposit_money'),
    path("report/", TransactionReportView.as_view(), name="transaction_report"),
    path("loan_request/", LoanRequestView.as_view(), name="loan_request"),
    path("loans/", LoanListView.as_view(), name="loan_list"),
    path("loans/<int:loan_id>/", PayLoanView.as_view(), name="pay"),
    path('transfer/', TransferView.as_view(), name='transfer_money'),

]
