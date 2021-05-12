from os import name
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from Cartes_Creditss.models import credit_card
from comptess.models import Account
from django.contrib.auth.models import User
from transactiions.models import Transactiions
import pickle




def ListeTransactions(request):

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
        
    
    context = {'listetransactions': ListeTransactions }

    return render(request, 'transactions.html',context)


'''def fraudDetection():
    # Load from file
    pkl_filename = "C:/pickle_modelFraud.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
        
    listTransactions = Transactiions.objects.all()

    for i in listTransactions :
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

        X_test = [amt,category,hours,dob,month,gender,unix_time,year,day,city_pop]   

        Ypredict = pickle_model.predict(X_test)  

fraudDetection()'''



