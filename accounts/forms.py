from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE,GENDER_TYPE
from .models import UserAddress,UserBankAccount
class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    # we use widget to get the date input and give the type date attrs
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    # Instated of charfield in form we have to use ChoiceField to get the choices
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE) 
    country = forms.CharField(max_length =100)
    city = forms.CharField(max_length= 100)
    street_address = forms.CharField(max_length= 100)
    postal_code = forms.IntegerField()
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name',
        'last_name', 'email', 'account_type', 'birth_date','gender', 'postal_code',
        'city','country', 'street_address']
        # this all filed we be visible to the user .
    def save(self, commit=True) -> Any:
        our_user =  super().save(commit = False)
        if (commit == True ):
            our_user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            country = self.cleaned_data.get('country')
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')
            postal_code = self.cleaned_data.get('postal_code')
           
            UserAddress.objects.create(
                user = our_user,
                country = country,
                city = city, 
                street_address = street_address,
                postal_code = postal_code
            )
            UserBankAccount.objects.create(
                user = our_user,
                account_type = account_type ,
                gender = gender,
                birth_date = birth_date,
                account_no = 120000 + our_user.id

            )
        return our_user

