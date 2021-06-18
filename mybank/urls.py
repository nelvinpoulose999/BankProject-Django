"""BankProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import Registeration,Login,AccountCreateView,index,TransationView,BalanceView,TransactionHistoryView,Signout,\
    myhomepage,UserDetailsView,UserUpdateView
urlpatterns = [
    path('register',Registeration.as_view(),name='register'),
    path('',Login.as_view(),name='login'),
    path('accounts',AccountCreateView.as_view(),name='accounts'),
    path('index',index,name='index'),
    path('transactions',TransationView.as_view(),name='transactions'),
    path('enq',BalanceView.as_view(),name='balance'),
    path('history',TransactionHistoryView.as_view(),name='history'),
    path('logout',Signout.as_view(),name='logout'),
    path('base1',myhomepage,name='base1'),
    path('details', UserDetailsView.as_view(), name='details'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update')
]
