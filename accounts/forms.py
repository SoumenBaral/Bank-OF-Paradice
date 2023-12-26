from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE,GENDER_TYPE
from .models import UserAddress,UserBankAccount
class UserRegistrationForm(UserCreationForm): #we Inherited the form from the UserCreation Form 
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
        # this all filed we be visible to the user . password two is the confirm Password 
    def save(self, commit=True) -> Any: 
        # if give proper info then we give the permission to go on save's default commit is true
        # but if we want to do so more thing so we are not using default save function .
        our_user =  super().save(commit = False)  
        # we are not interested to save the user NOW
        if (commit == True ):
            our_user.save() 
            # We save user model's data save 
            account_type = self.cleaned_data.get('account_type')
            # we use clean data to get the data from database 
            gender = self.cleaned_data.get('gender')
            # get function is allow one data at a time and its have to be unique 
            birth_date = self.cleaned_data.get('birth_date')
            country = self.cleaned_data.get('country')
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')
            postal_code = self.cleaned_data.get('postal_code')
           
            UserAddress.objects.create( # create a userAddress Objects

                user = our_user, # first is form model and second is we get the data using the clear data get
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
                # we create a account number Automatically add the user id with a random number 

            )
        
        return our_user
    def __init__(self, *args, **kwargs):
# The method is used to initialize the attributes or perform any setup that is necessary for instances of the class.
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({ # we add the class for every Attribute's class 
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })
   

class UserUpdateForm(forms.ModelForm):
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
        fields = ['first_name','last_name','email']
     
    def __init__(self, *args, **kwargs):
        # The method is used to initialize the attributes or perform any setup that is necessary for instances of the class.
        super().__init__(*args,**kwargs)
        # super will be inherit the init function that is contractor of this class

        for field in self.fields:
            self.fields[field].widget.attrs.update({ # we add the class for every Attribute's class 
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })

        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserBankAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['account_type'].initial = user_account.account_type
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country
    def save(self, commit = True) -> Any:
        user = super().save(commit=False)
        if commit:
            user.save()
            user_account, created = UserBankAccount.objects.get_or_create(user=user)
            # if user is true then get the user if not  create the user 
            user_address, created = UserAddress.objects.get_or_create(user=user) 
            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user

    