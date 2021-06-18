from django.contrib.auth import authenticate,login as djangologin,logout
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .forms import UserRegisterationForm,UserLoginForm,AccountCreationForm,TransationCreateForm,AccountEditForm,UserUpdateForm
from .models import CustomUser,Account,Transactions
from django.utils.decorators import method_decorator
from .decorators import account_validator,user_login
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

@user_login
def myhomepage(request):
    context = {}
    try:
        account = Account.objects.get(user=request.user)
        flag = True if account else False
        context['flag'] = flag
        return render(request, 'mybank/base1.html', context)
    except:
        return render(request, 'mybank/base1.html',context)

class Registeration(TemplateView):
    model = CustomUser
    template_name = 'mybank/registeration.html'
    form_class = UserRegisterationForm
    context = {}
    def get(self,request,*args,**kwargs):
        self.context['form'] = self.form_class
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            self.context['forms']=form
            return render(request, self.template_name, self.context)

class Login(TemplateView):
    model = CustomUser
    template_name = 'mybank/login.html'
    form_class = UserLoginForm
    context = {}
    def get(self, request, *args, **kwargs):
        # try:
            # userid=CustomUser.objects.get(user=request.user)
            # flag = True if userid else False
            self.context['form'] = self.form_class()
            return render(request, self.template_name, self.context)
        # # except:
        #     form=self.form_class()
        #     return render(request, self.template_name, {'form':form})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            print(username,password)
            try:
                user = self.model.objects.get(username=username)
                # if (user.username==username) & (user.username==username)
                if(user.username==username):
                    if (user.password==password):
                        djangologin(request,user)
                        # print('success')
                        return redirect('index')
                    else:
                        messages.error(request, 'Password incorrect')
                        return render(request, self.template_name, self.context)
                else:
                    messages.error(request, 'Username not correct')
                    # print('failed')
                    return render(request, self.template_name, self.context)
            except:
                messages.error(request, 'Username not correct')
                print('failed')
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, self.context)

@user_login
def index(request):
    context={}
    try:
        account = Account.objects.get(user=request.user)
        # status = account.active_status
        # flag = True if (status == 'active')  else False
        flag= True if account else False
        context['flag'] = flag
        return render(request, 'mybank/base1.html', context)
    except:
        return render(request, 'mybank/base1.html', context)

@method_decorator(user_login,name='dispatch')
@method_decorator(account_validator,name='dispatch')
class AccountCreateView(TemplateView):
    model=Account
    template_name = 'mybank/useraccount.html'
    form_class=AccountCreationForm
    context={}
    def get(self, request, *args, **kwargs):
        account_number=""
        account=self.model.objects.all().last()
        if account:
            acno=int(account.account_number.split('-')[1])+1
            account_number='sbk-'+str(acno)
        else:
            account_number='sbk-1000'
        self.context['form']=self.form_class(initial={'account_number':account_number,'user':request.user})
        return render(request,self.template_name,self.context)


    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print('failed')
            self.context['form']=form
            return render(request, self.template_name, self.context)

class GetUserMixin(object):
    def get_user(self,account_num):
        return Account.objects.get(account_number=account_num)

@method_decorator(user_login,name='dispatch')
class TransationView(TemplateView,GetUserMixin):
    model=Transactions
    template_name = 'mybank/moneytransfer.html'
    form_class=TransationCreateForm
    context={}
    def get(self, request, *args, **kwargs):
        try:
            currentaccount=Account.objects.get(user=request.user)
            flag = True if currentaccount else False
            status=currentaccount.active_status
            if status=='inactive':
                msg='Account is not activated'
                return render(request, self.template_name, {' msg':  msg,'flag':flag})
            else:
                form = self.form_class(initial={'user': request.user})
                return render(request, self.template_name, {'form':form,'flag':flag})
        except:
            msg='Sorry,No Account'
            # self.context['form'] = self.form_class(initial={'user': request.user})
            return render(request, self.template_name, {' msg':  msg})

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            to_account=form.cleaned_data.get('to_account_number')
            amount=form.cleaned_data.get('amount')
            remarks=form.cleaned_data.get('remarks')
            account=self.get_user(to_account)
            if account.active_status=='active':
                account.balance+=int(amount)
                account.save()
                currentaccount=Account.objects.get(user=request.user)
                currentaccount.balance-=int(amount)
                currentaccount.save()
                transaction=Transactions(user=request.user,amount=amount,to_account=to_account,remarks=remarks)
                transaction.save()
                # messages.success(request, 'Transaction Successful')
                return redirect('index')
            else:
                messages.error(request, 'Invalid Account')
                self.context['form'] = form
                return render(request, self.template_name, self.context)
        else:
            self.context['form']=form
            return render(request, self.template_name, self.context)

@method_decorator(user_login,name='dispatch')
class BalanceView(TemplateView):
    def get(self, request, *args, **kwargs):
        account=Account.objects.get(user=request.user)
        balance=account.balance
        print(balance)
        return JsonResponse({'balance':balance})
        # return render(request,'mybank/base1.html', {'balance':balance})

@method_decorator(user_login,name='dispatch')
class TransactionHistoryView(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            debit_transactions=Transactions.objects.filter(user=request.user)
            l_user=Account.objects.get(user=request.user)
            flag = True if l_user else False
            credit_transactions=Transactions.objects.filter(to_account=l_user.account_number)
            return render(request, 'mybank/userhistory.html',{'dtransactions': debit_transactions,
                                                              'ctransactions': credit_transactions,'flag':flag})

        except:
            message='No Account'
            return render(request,'mybank/userhistory.html',{'message':message})

class Signout(TemplateView):
    def get(self,request):
        logout(request)
        return redirect('login')

@method_decorator(user_login,name='dispatch')
class UserDetailsView(TemplateView):
    def get(self, request,*args, **kwargs):
        try:
            details=Account.objects.get(user=request.user)
            flag=True if details else False
            udetails=CustomUser.objects.get(username=request.user)
            return render(request, 'mybank/userdetails.html', {'details':details,'udetails':udetails,'flag': flag})
        except:
            udetails = CustomUser.objects.get(username=request.user)
            return render(request, 'mybank/userdetails.html', {'udetails':udetails})

@method_decorator(user_login,name='dispatch')
class UserUpdateView(TemplateView):
    model_account = Account
    model_user =CustomUser
    template_name = 'mybank/userupdate.html'
    userform_class = UserUpdateForm
    accountform_class=AccountEditForm
    context = {}

    def get(self,request,*args, **kwargs):
        id=kwargs.get('pk')
        try:
            userupdate=self.model_user.objects.get(id=id)
            accountedit=self.model_account.objects.get(user_id=userupdate.id)
            flag=True if accountedit else False
            userform=self.userform_class(instance=userupdate)
            accountform=self.accountform_class(instance=accountedit)
            return render(request, self.template_name, {'userform': userform,'accountform': accountform, 'flag': flag})
        except:
            userupdate = self.model_user.objects.get(id=id)
            userform = self.userform_class(instance=userupdate)
            return render(request, self.template_name,{'userform': userform})

    def post(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        try:
            userupdate = self.model_user.objects.get(id=id)
            accountedit = self.model_account.objects.get(user_id=userupdate.id)
            userform = self.userform_class(request.POST, instance=userupdate)
            accountform = self.accountform_class(request.POST, instance=accountedit)
            if userform.is_valid() & accountform.is_valid():
                userform.save()
                accountform.save()
                return redirect('details')
            else:
                return render(request, self.template_name, {'userform': userform,'accountform': accountform})
        except:
            userupdate = self.model_user.objects.get(id=id)
            userform = self.userform_class(request.POST, instance=userupdate)
            if userform.is_valid():
                userform.save()
                return redirect('details')



