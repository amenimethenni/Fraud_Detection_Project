

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser :
                    login(request, user)
                    #return redirect("/")
                    return render(request, "ui-notifications.html", {"form": form})
                else :
                    login(request, user)
                    #return redirect("/")
                    return render(request, "dashboard.html", {"form": form})


            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'Utilisateur crée avec succès.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })


###########ListeUser##############""
from django.contrib.auth import get_user_model
from transactiions.models import Transactiions
from Cartes_Creditss.models import credit_card
from comptess.models import Account
from django.contrib.auth.models import User
import pickle
from sklearn.preprocessing import LabelEncoder
from pandas import DataFrame
import pandas as pd 

def users(request):

    User = get_user_model()
    users = User.objects.filter(is_superuser = 0) 
    
    ####piechart H&F#########  
    female_count  =Transactiions.objects.filter(gender='F').count()
    men_count  =Transactiions.objects.filter(gender='M').count()

    ####Liste transaction#########  
    user = User.objects.get(username=request.user.username)

    ############### Get account For  User Connected ##########################

    account = Account.objects.filter(user=user)
    accountuser = Account.objects.all()

    listCards=[]
    ListeTransactions=[]

    listCardss=[]
    ListeTransactionss=[]

    ############### Get List Of Credit Card ##########################
    for acc in list(account):
        listCards.append(credit_card.objects.get(compte=acc))
    
    for acc in list(accountuser):
        listCardss.append(credit_card.objects.get(compte=acc))

    ############### Get List Of Transactions ##########################

    for card in listCards:
      
        listTrans=Transactiions.objects.filter(CarteCredit=card)
        for i in listTrans :
            ListeTransactions.append(i)

    
    for card in listCardss:
      
        listTransa=Transactiions.objects.filter(CarteCredit=card)
        for i in listTransa :
            ListeTransactionss.append(i)


    context = {'users': users ,'female_count': female_count,'men_count':men_count  ,'listetransactions': ListeTransactions,'ListeTransactionss':ListeTransactionss}


    return render(request, 'ui-notifications.html',context)

####get List user###############
def getlisteuser (request) :
    
    User = get_user_model()
    getlisteuser = User.objects.filter(is_superuser = 0)
    context = {'getlisteuser': getlisteuser}


    return render(request, 'getlisteuser.html',context)

    



