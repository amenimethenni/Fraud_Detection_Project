from os import name
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from Cartes_Creditss.models import credit_card
from comptess.models import Account
from django.contrib.auth.models import User
from transactiions.models import Transactiions
import pickle
from sklearn.preprocessing import LabelEncoder



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

    ####FraudModel############
    '''pkl_filename = "C:/pickle_modelFraud.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
           
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
        ## séparer les données catégoriques et numériques
        num_data =  [amt,hours,month,unix_time,year,day,city_pop]
        cat_data = [category,dob,gender]
         # Remplacer les valeurs catégoriques par des valeurs numériques
        le=LabelEncoder()
        for j in cat_data :
            cat_data[j]=le.fit_transform(cat_data[j])
        X_test_prep= [*cat_data, *num_data]
        Ypredict = pickle_model.predict(X_test_prep)

        if Ypredict is not None :
            i.is_fraud_pred = Ypredict'''

    context = {'listetransactions': ListeTransactions  }

    return render(request, 'transactions.html',context)



        
