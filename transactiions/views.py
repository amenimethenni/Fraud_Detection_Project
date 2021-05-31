from mmap import ALLOCATIONGRANULARITY
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
from django.contrib.auth import logout

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

    ##dataframe 
    dffinal = PreprocessingCateg(df)
    dffinalfraud = PreprocessingFraud(df)
    
    ####liste des transactions
    alllist=[]
    alllistfraud=[]
    for i in ListeTransactions :
        alllist.append([i.merchant,i.amt,i.dob,i.hours])
        alllistfraud.append([i.amt,i.category,i.hours,i.dob,i.month,i.gender,i.unix_time, i.year,i.day,i.city_pop])
    

    newdf = pd.DataFrame(alllist)
    newdffraud = pd.DataFrame(alllistfraud)
    newdf.columns = ["merchant","amt","dob","hours"]
    newdffraud.columns = ['amt','category','hours','dob','month','gender','unix_time', 'year','day','city_pop'] 
    newdffraud.columns = ['amt','category','hours','dob','month','gender','unix_time', 'year','day','city_pop'] 
           
    dffinal = pd.concat([dffinal,newdf], ignore_index=True)
    dffinalfraud = pd.concat([dffinalfraud,newdffraud], ignore_index=True)
                 
    ##labelEncoder 
    le=LabelEncoder()
    for i in dffinal :     
        dffinal['merchant']=le.fit_transform(dffinal['merchant'].astype(str))                
        dffinal['dob']=le.fit_transform(dffinal['dob'].astype(str)) 
        #print ('dffinal',dffinal)

    ##labelEncoder fraud detection##
    
    for i in dffinalfraud :     
        dffinalfraud['category']=le.fit_transform(dffinalfraud['category'].astype(str))                
        dffinalfraud['gender']=le.fit_transform(dffinalfraud['gender'].astype(str)) 
        dffinalfraud['dob']=le.fit_transform(dffinalfraud['dob'].astype(str)) 
        

    ####convert df to list#######
  
    newdf=dffinal.tail(len(newdf))
    new_df_categ = newdf.values.tolist() 

    newdffraud =dffinalfraud.tail(len(newdffraud))
    new_df_fraud = newdffraud.values.tolist()


    ### category Prediction####
    listpredcat=[]
    listpredfraud=[]
    for i in new_df_categ:
        YpredictCategory = pickle_modelCateg.predict([i])
        listpredcat.append(YpredictCategory[0])

    for i,j in zip(ListeTransactions,listpredcat):
        if (i.category is None):
            i.category_pred=j
            i.save()
    
    ### fraud Prediction####
        
    for i in new_df_fraud:
        Ypredictfraud = pickle_modelFraud.predict([i])
        listpredfraud.append(Ypredictfraud[0])

    for i,j in zip(ListeTransactions,listpredfraud):
        i.is_fraud_pred=j
        i.save()
        '''if ((i.is_fraud_pred ==1 ) or (i.is_fraud == 1)):
            i.etat = True
            i.save()
            redirect ("accounts/login.html")'''
    context = {'listetransactions': ListeTransactions  }

    return render(request, 'transactions.html',context)


def fraudupdate (request):
    
    user = User.objects.get(username=request.user.username)

    account = Account.objects.filter(user=user)
    account.etat = True
    account.save() 
    
  

    return render(request, 'accounts/login.html')

    
    
  


    






###preprocess category prediction##########
df = pd.read_csv('C:/fraudTest.csv',nrows= 20000 )

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








        
