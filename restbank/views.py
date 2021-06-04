from django.shortcuts import render
from rest_framework import generics,mixins

from mybank.models import Account,CustomUser,Transactions
from .serializer import UserRegisterationSerializer,AccountSerialiser

# Create your views here.
class Usermixinregister(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset =CustomUser.objects.all()
    serializer_class = UserRegisterationSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class AccountdetailmixinView(generics.GenericAPIView,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin):
    queryset = Account.objects.all()
    serializer_class =AccountSerialiser
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class TransactiondetailmixinView(generics.GenericAPIView,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin):
    queryset = Transactions.objects.all()
    serializer_class =AccountSerialiser
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


