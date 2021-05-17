
from transactiions.models import Transactiions
from django.shortcuts import render, redirect

def dashboard(request):

    shopping  =Transactiions.objects.filter(category='shopping').count()
    grocery  =Transactiions.objects.filter(category='grocery').count()
    misc  =Transactiions.objects.filter(category='misc').count()
    gas_transport  =Transactiions.objects.filter(category='gas_transport').count()
    home  =Transactiions.objects.filter(category='home').count()
    kids_pets  =Transactiions.objects.filter(category='kids_pets').count()
    entertainment  =Transactiions.objects.filter(category='entertainment').count()
    food_dining   =Transactiions.objects.filter(category='food_dining').count()
    personal_care  =Transactiions.objects.filter(category='personal_care').count()
    health_fitness =Transactiions.objects.filter(category='health_fitness').count()
    travel  =Transactiions.objects.filter(category='travel').count()

    context = {'shopping':shopping,'grocery':grocery,'misc':misc,'gas_transport':gas_transport,'home':home,'kids_pets':kids_pets,'entertainment':entertainment,
    'food_dining':food_dining,'personal_care':personal_care,'health_fitness':health_fitness,'travel':travel}

    return render(request, 'dashboard.html',context)

from django.contrib.auth import get_user_model
from Cartes_Creditss.models import credit_card
from comptess.models import Account
from django.contrib.auth.models import User

def listetransactFraud (request):
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
    
    ####detailles transact frauduleuse#########  
    #fraude  =Transactiions.objects.filter(is_fraud='1').count()
    #Not_fraud  =Transactiions.objects.filter(is_fraud='0').count()
    context = {'users': users ,'ListeTransactions':ListeTransactions}


    return render(request, 'listetransactFraud.html',context)