
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

    User = get_user_model()
    users = User.objects.all()  

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
            
    
    items1  =Transactiions.objects.filter(category='shopping')
    shopping = sum(items1.values_list('amt', flat=True))

    items2  =Transactiions.objects.filter(category='grocery')
    grocery  =sum(items2.values_list('amt', flat=True))

    items3  =Transactiions.objects.filter(category='misc')
    misc  =sum(items3.values_list('amt', flat=True))

    items4  =Transactiions.objects.filter(category='gas_transport')
    gas_transport  =sum(items4.values_list('amt', flat=True))

    items5  =Transactiions.objects.filter(category='home')
    home  = sum(items5.values_list('amt', flat=True))

    items6  =Transactiions.objects.filter(category='kids_pets')
    kids_pets  = sum(items6.values_list('amt', flat=True))

    items7  =Transactiions.objects.filter(category='entertainment')
    entertainment  =sum(items7.values_list('amt', flat=True))

    items8  =Transactiions.objects.filter(category='food_dining')
    food_dining   =sum(items8.values_list('amt', flat=True))

    items9  =Transactiions.objects.filter(category='personal_care')
    personal_care  =sum(items9.values_list('amt', flat=True))

    items10  =Transactiions.objects.filter(category='health_fitness')
    health_fitness =sum(items10.values_list('amt', flat=True))

    items11  =Transactiions.objects.filter(category='travel')
    travel  = sum(items11.values_list('amt', flat=True))


    context = {'shopping':shopping,'grocery':grocery,'misc':misc,'gas_transport':gas_transport,'home':home,'kids_pets':kids_pets,'entertainment':entertainment,
    'food_dining':food_dining,'personal_care':personal_care,'health_fitness':health_fitness,'travel':travel}

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

     # Load FraudModel
    pkl_filenameFraud = "c:/PredictionFraud.sav"
    with open(pkl_filenameFraud, 'rb') as file:
        pickle_modelFraud = pickle.load(file)
    #Load CategModel
    pkl_filenameCateg = "c:/pickle_modelcateg.pkl"
    with open(pkl_filenameCateg, 'rb') as file:
        pickle_modelCateg = pickle.load(file)
           
    for i in ListeTransactions :
        amt = i.amt
        category = i.category
        hours = i.hours
        dob = i.dob
        month = i.month
        gender = i.gender
        unix_time = i.unix_time
        year = i.year
        day = i.day
        city_pop = i.city_pop
        merchant = i.merchant


            
    context = {'listetransactions': ListeTransactions  }


    return render(request, 'navigation.html',context)
