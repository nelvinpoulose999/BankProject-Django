from django.forms import ModelForm
from django import forms
from mybank.models import CustomUser,Account,Transactions


class UserRegisterationForm(ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}),label='')
    class Meta:
         model=CustomUser
         fields=['username','first_name','last_name','email','date_joined','phone_number','age','password']

         widgets = {
                'username': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Username'}),
                'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Lastname'}),
                'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Id'}),
                'date_joined': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date of Joining'}),
                'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
                'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Age'}),

                }


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),label='')


class AccountCreationForm(ModelForm):
    class Meta:
        model=Account
        fields=['account_number','balance','ac_type','user','active_status']
        widgets={
            'account_number':forms.TextInput(attrs={'readonly':True,'class': 'form-control'}),
            'user':forms.Select(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Balance'}),
            'ac_type': forms.Select(attrs={'class': 'form-control'}),
            'active_status': forms.Select(attrs={'class': 'form-control'})
        }
class TransationCreateForm(forms.Form):
    user = forms.CharField()
    to_account_number = forms.CharField(widget=forms.PasswordInput)
    confirm_account_number = forms.CharField()
    amount=forms.CharField(max_length=5)
    remarks=forms.CharField()

    user = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), label='')
    to_account_number = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Account Number'}),label='')
    confirm_account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Account'}),label='')
    amount = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),label='')
    remarks = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Remarks'}),label='')


    def clean(self):
        cleaned_data = super().clean()
        to_account_number=cleaned_data.get('to_account_number')
        confirm_account_number=cleaned_data.get('confirm_account_number')
        amount=cleaned_data.get('amount')
        user=cleaned_data.get('user')
        try:
            account=Account.objects.get(account_number=to_account_number)
        except:
            msg = 'Account number mismatch'
            self.add_error('to_account_number', msg)

        if to_account_number!=confirm_account_number:
            msg='Account number mismatch'
            self.add_error('to_account_number',msg)

        account=Account.objects.get(user__username=user)
        avlbalance=account.balance
        if int(amount)>int(avlbalance):
            message='Insufficient balance'
            self.add_error('amount',message)

