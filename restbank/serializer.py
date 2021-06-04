from rest_framework import serializers
from mybank.models import Account,CustomUser,Transactions
from rest_framework.serializers import ModelSerializer

class UserRegisterationSerializer(ModelSerializer):
    class Meta:
         model=CustomUser
         fields=['username','first_name','last_name','email','date_joined','phone_number','age','password']


class AccountSerialiser(ModelSerializer):
    class Meta:
        fields = ['account_number', 'balance', 'ac_type', 'user', 'active_status']

class TransactionSerialiser(ModelSerializer):
    class Meta:
        fields = ['user', 'to_account_number', 'confirm_account_number', 'amount', 'remarks']