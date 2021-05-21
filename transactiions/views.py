from os import name
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from Cartes_Creditss.models import credit_card
from comptess.models import Account
from django.contrib.auth.models import User
from transactiions.models import Transactiions
import pickle
from sklearn.preprocessing import LabelEncoder
from pandas import DataFrame
import pandas as pd




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

     # Load FraudModel
    pkl_filenameFraud = "c:/PredictionFraud.sav"
    with open(pkl_filenameFraud, 'rb') as file:
        pickle_modelFraud = pickle.load(file)
    #Load CategModel
    pkl_filenameCateg = "c:/pickle_modelcateg.pkl"
    with open(pkl_filenameCateg, 'rb') as file:
        pickle_modelCateg = pickle.load(file)

    ##dataframe (4 colonnes )
    dffinal = PreprocessingCateg(df)
    dffinalfraud = PreprocessingFraud(df)
    
    ####liste des transactions
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

        ###df CategoryPrediction###
        listeCategoryPrediction = [merchant,amt,dob,hours]
        dfCategoryPrediction= DataFrame (listeCategoryPrediction).transpose()
        dfCategoryPrediction.columns = ['merchant','amt','dob','hours']   

         ###df FraudPrediction###
        listeFraudPrediction = [amt,category,hours,dob,month,gender,unix_time, year,day,city_pop]
        dffraudPrediction= DataFrame (listeFraudPrediction).transpose()
        dffraudPrediction.columns = ['amt','category','hours','dob','month','gender','unix_time', 'year','day','city_pop']       
        
        ##Append dfCategoryPrediction to dataframe original####
        
        dffinal = pd.concat([dffinal,dfCategoryPrediction], ignore_index=True)

        ##Append dffraudPrediction to dataframe original####
        
        dffinalfraud = pd.concat([dffinalfraud,dffraudPrediction], ignore_index=True)
                
        ##labelEncoder category prediction##
        le=LabelEncoder()
        for i in dffinal :     
            dffinal['merchant']=le.fit_transform(dffinal['merchant'].astype(str))                
            dffinal['dob']=le.fit_transform(dffinal['dob'].astype(str)) 
        print ('dffinal',dffinal)

        ##labelEncoder fraud detection##
        le=LabelEncoder()
        for i in dffinalfraud :     
            dffinalfraud['category']=le.fit_transform(dffinalfraud['category'].astype(str))                
            dffinalfraud['gender']=le.fit_transform(dffinalfraud['gender'].astype(str)) 
            dffinalfraud['dob']=le.fit_transform(dffinalfraud['dob'].astype(str)) 
        print ('dffinalfraud',dffinalfraud)

        ####convert df to list#######

        listefinalcategory = dffinal.values.tolist()  
        #print('listefinalcategory',listefinalcategory)
        
        listefinalFraud = dffinalfraud.values.tolist()  
        #print('listefinal',listefinalFraud)

        ### category Prediction#####
        '''YpredictCategory = pickle_modelCateg.predict(listefinalcategory)
        #print('YpredictCategory',YpredictCategory)        
        if YpredictCategory is not None   :
            i.category_pred = YpredictCategory

        ###Fraud detection#####
        YpredictFraud = pickle_modelFraud.predict(listefinalFraud)
        #print('YpredictFraud',YpredictFraud)
        if YpredictFraud is not None :
            i.is_fraud_pred = YpredictFraud'''
        
            
    context = {'listetransactions': ListeTransactions  }

    return render(request, 'transactions.html',context)


###preprocess category prediction##########
df = pd.read_csv('C:/fraudTest.csv')

def PreprocessingCateg(df):
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['year'] = df['trans_date_trans_time'].dt.year
    df['month'] = df['trans_date_trans_time'].dt.month
    df['day'] = df['trans_date_trans_time'].dt.day
    df['hours'] = df['trans_date_trans_time'].dt.hour  
    df['minutes'] = df['trans_date_trans_time'].dt.minute
    df['secondes'] = df['trans_date_trans_time'].dt.second
    df['category'] = df['category'].replace(['grocery_pos'],'grocery')
    df['category'] = df['category'].replace(['grocery_net'],'grocery')
    df['category'] = df['category'].replace(['misc_pos'],'misc')
    df['category'] = df['category'].replace(['misc_net'],'misc')
    df['category'] = df['category'].replace(['shopping_pos'],'shopping')
    df['category'] = df['category'].replace(['shopping_net'],'shopping')
    df = df.drop('trans_date_trans_time',axis=1)
    df = df.drop('last',axis=1)
    df = df.drop('first',axis=1)
    df = df.drop('city',axis=1)
    df = df.drop('Unnamed: 0', axis=1)
    df = df.drop ('is_fraud',axis=1)
    df = df.drop ('zip',axis=1)
    df = df.drop ('lat',axis=1)
    df = df.drop ('long',axis=1)
    df = df.drop ('city_pop',axis=1)
    df = df.drop ('unix_time',axis=1)
    df = df.drop ('merch_lat',axis=1)
    df = df.drop ('merch_long',axis=1)
    df = df.drop ('year',axis=1)
    df = df.drop ('month',axis=1)
    df = df.drop ('day',axis=1)
    df = df.drop ('minutes',axis=1)
    df = df.drop ('secondes',axis=1)
    df = df.drop ('category',axis=1)
    df = df.drop ('gender',axis=1)
    df = df.drop ('street',axis=1)
    df = df.drop ('state',axis=1)
    df = df.drop ('job',axis=1)
    df = df.drop ('trans_num',axis=1)
    df = df.drop ('cc_num',axis=1)

    return df


###preprocess Fraud detection##########


def PreprocessingFraud(df):

    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['year'] = df['trans_date_trans_time'].dt.year
    df['month'] = df['trans_date_trans_time'].dt.month
    df['day'] = df['trans_date_trans_time'].dt.day
    df['hours'] = df['trans_date_trans_time'].dt.hour  
    df['minutes'] = df['trans_date_trans_time'].dt.minute
    df['secondes'] = df['trans_date_trans_time'].dt.second
    df['category'] = df['category'].replace(['grocery_pos'],'grocery')
    df['category'] = df['category'].replace(['grocery_net'],'grocery')
    df['category'] = df['category'].replace(['misc_pos'],'misc')
    df['category'] = df['category'].replace(['misc_net'],'misc')
    df['category'] = df['category'].replace(['shopping_pos'],'shopping')
    df['category'] = df['category'].replace(['shopping_net'],'shopping')
    df = df.drop('trans_date_trans_time',axis=1)
    df = df.drop('last',axis=1)
    df = df.drop('first',axis=1)
    df = df.drop('city',axis=1)
    df = df.drop('Unnamed: 0', axis=1)
    df = df.drop ('is_fraud',axis=1)
    df = df.drop ('zip',axis=1)
    df = df.drop ('lat',axis=1)
    df = df.drop ('long',axis=1)
    df = df.drop ('merch_lat',axis=1)
    df = df.drop ('merch_long',axis=1)
    df = df.drop ('minutes',axis=1)
    df = df.drop ('secondes',axis=1)
    df = df.drop ('street',axis=1)
    df = df.drop ('state',axis=1)
    df = df.drop ('job',axis=1)
    df = df.drop ('trans_num',axis=1)
    df = df.drop ('cc_num',axis=1)
    df = df.drop ('merchant',axis=1)

    return df




        
