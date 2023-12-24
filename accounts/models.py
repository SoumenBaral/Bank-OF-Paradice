from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE,GENDER_TYPE

class UserBankAccount(models.Model):
    user = models.OneToOneField(User,related_name ="Account",on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique = True)
    birth_date = models.DateField(null = True,blank = True)
    gender = models.CharField(max_length=10,choices=GENDER_TYPE)
    initial_deposit_date = models.DateField(auto_now_add = True)
    balance = models.DecimalField(max_digits=12, decimal_places=2,null=True)

    def __str__(self) -> str:
        return str(self.account_no)
        
class UserAddress(models.Model):
    user = models.OneToOneField(User,related_name ="Address",on_delete=models.CASCADE)
    country = models.CharField(max_length =100)
    city = models.CharField(max_length= 100)
    street_address = models.CharField(max_length= 100)
    postal_code = models.IntegerField()

    def __str__(self) -> str:
        return self.user.email





