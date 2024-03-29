
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from .constants import ACCOUNT_TYPE,GENDER_TYPE 

class UserBankAccount(models.Model):
    user = models.OneToOneField(User,related_name ="account",on_delete=models.CASCADE)
    # this user make one to one relations with Current logged in user 
    # we use to related name to Access user via the name Account . 
    # we know the work of on delete  when we delete on Another will be Automatically delete 
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    # We use a character field as choices field and Account type come from constants 
    account_no = models.IntegerField(unique = True)
    # Account Number will be unique for every user
    birth_date = models.DateField(null = True,blank = True)
    gender = models.CharField(max_length=10,choices=GENDER_TYPE)
    initial_deposit_date = models.DateField(auto_now_add = True)
    balance = models.DecimalField(max_digits=12, decimal_places=2,default=Decimal('0.00'))

    def __str__(self) -> str:
        return str(self.account_no)
    #  via str function we are able to see the value on of an return element 
        
class UserAddress(models.Model):
    user = models.OneToOneField(User,related_name ="address",on_delete=models.CASCADE)
    country = models.CharField(max_length =100)
    city = models.CharField(max_length= 100)
    street_address = models.CharField(max_length= 100)
    postal_code = models.IntegerField()

    def __str__(self) -> str:
        return self.user.email
    
    # Str Dander Method ha ha ha 

class isBankCraft(models.Model):
    Is_Bank_Craft = models.BooleanField(default=False)




