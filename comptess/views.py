
from transactiions.models import Transactiions
from django.shortcuts import render, redirect
import pickle
from sklearn.preprocessing import LabelEncoder
from pandas import DataFrame
import pandas as pd
from django.contrib.auth import get_user_model
from Cartes_Creditss.models import credit_card
from comptess.models import Account
from django.contrib.auth.models import User
from django.db.models import Sum


def dashboard(request):
    
    personal_care = 0 
    shopping = 0
    grocery = 0
    misc = 0
    gas_transport = 0
    home = 0
    kids_pets = 0
    entertainment = 0
    food_dining = 0
    health_fitness = 0
    travel = 0

    

    ####Liste transaction#########  
    user = User.objects.get(username=request.user.username)

    ############### Get account For  User Connected ##########################

    account = Account.objects.filter(user=user)

    listCards=[]
    ListeTransactions=[]

    ############### Get List Of Credit Card ##########################
    for acc in list(account):
        listCards.append(credit_card.objects.get(compte=acc))

    ############### Get List Of Transactions ##########################

    for card in listCards:
      
        listTrans=Transactiions.objects.filter(CarteCredit=card)
        for i in listTrans :
            ListeTransactions.append(i)

    for i in ListeTransactions :
        
        if ((i.category == "personal_care") or (i.category_pred == "8")):
            personal_care = personal_care + i.amt           
        elif ((i.category == "shopping") or (i.category_pred == "9")):
            shopping = shopping + i.amt
        elif ((i.category == "grocery") or (i.category_pred == "3")):
            grocery = grocery + i.amt
                    
        elif ((i.category == "misc") or (i.category_pred == "7")):
            misc = misc + i.amt

        elif ((i.category == "gas_transport") or (i.category_pred == "2")):
            gas_transport = gas_transport + i.amt
        
        elif ((i.category == "gas_transport") or (i.category_pred == "2")):
            gas_transport = gas_transport + i.amt

        elif ((i.category == "home") or (i.category_pred == "5")):
            home = home + i.amt
        elif ((i.category == "kids_pets") or (i.category_pred == "6")):
            kids_pets = kids_pets + i.amt
        elif ((i.category == "entertainment") or (i.category_pred == "0")):
            entertainment = entertainment + i.amt
        elif ((i.category == "food_dining") or (i.category_pred == "1")):
            food_dining = food_dining + i.amt
        elif ((i.category == "travel") or (i.category_pred == "10")):
            travel = travel + i.amt
        elif ((i.category == "health_fitness") or (i.category_pred == "4")):
            health_fitness = health_fitness + i.amt
        liste =[shopping,grocery,misc,gas_transport,home,kids_pets,entertainment,food_dining,personal_care,health_fitness,travel]
        listedepenses = (shopping+grocery+misc+gas_transport+home+kids_pets+entertainment+food_dining+personal_care+health_fitness+travel)

    mt = 0
    mtt = 0
    mttt = 0
    mt5 = 0
    for i in ListeTransactions :
        if (i.month == 6):
            mt = mt + i.amt
        elif (i.month == 4):
            mtt = mtt +i.amt
        elif (i.month == 7) :
            mttt= mttt +i.amt
        elif (i.month == 5):
            mt5=mt5+i.amt
        li = [mt,mtt,mttt,mt5] 


    context = {'ListeTransactions' : ListeTransactions,'liste':liste,'li':li,'listedepenses':listedepenses}

    return render(request, 'dashboard.html',context)


################listetransactFraud###########

def listetransactFraud (request):
    User = get_user_model()
    users = User.objects.all()

    ####Liste transaction#########  
    #user = User.objects.get(username=request.user.username)

    ############### Get account For  User Connected ##########################

    account = Account.objects.all()

    listCards=[]
    ListeTransactions=[]

    ############### Get List Of Credit Card ##########################
    for acc in list(account):
        listCards.append(credit_card.objects.get(compte=acc))

    ############### Get List Of Transactions ##########################

    for card in listCards:
      
        listTrans=Transactiions.objects.filter(CarteCredit=card)
        for i in listTrans :
            ListeTransactions.append(i)
    
    ####detailles transact frauduleuse#########  
    #fraude  =Transactiions.objects.filter(is_fraud='1').count()
    #Not_fraud  =Transactiions.objects.filter(is_fraud='0').count()
    context = {'users': users ,'listetransactions':ListeTransactions}


    return render(request, 'listetransactFraud.html',context)


    #########notif admin#############

def notifications (request) :
    
    
    User = get_user_model()
    users = User.objects.all()

    ####Liste transaction#########  
    #user = User.objects.get(username=request.user.username)

    ############### Get account For  User Connected ##########################

    account = Account.objects.all()

    listCards=[]
    ListeTransactions=[]

    ############### Get List Of Credit Card ##########################
    for acc in list(account):
        listCards.append(credit_card.objects.get(compte=acc))

    ############### Get List Of Transactions ##########################

    for card in listCards:
      
        listTrans=Transactiions.objects.filter(CarteCredit=card)
        for i in listTrans :
            ListeTransactions.append(i)
        
  
    ####detailles transact frauduleuse#########  
    #fraude  =Transactiions.objects.filter(is_fraud='1').count()
    #Not_fraud  =Transactiions.objects.filter(is_fraud='0').count()

    a = Transactiions.objects.all()
    context = {'listetransactions':ListeTransactions , 'users':users ,'a':a}

    return render(request, 'navigation.html',context)
