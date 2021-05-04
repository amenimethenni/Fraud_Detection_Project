import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit
import pickle



df = pd.read_csv('C:/fraudTrain.csv')

def PreprocessingFraud(df):
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['year'] = df['trans_date_trans_time'].dt.year
    df['month'] = df['trans_date_trans_time'].dt.month
    df['day'] = df['trans_date_trans_time'].dt.day
    df['hours'] = df['trans_date_trans_time'].dt.hour  
    df['minutes'] = df['trans_date_trans_time'].dt.minute
    df['secondes'] = df['trans_date_trans_time'].dt.second
    df = df.drop('trans_date_trans_time',axis=1)
    df = df.drop('last',axis=1)
    df = df.drop('first',axis=1)
    df = df.drop('city',axis=1)
    df = df.drop('Unnamed: 0', axis=1)
    # separer les données catégorique et numérique
    cat_data=[]
    num_data=[]
    for i,c in enumerate(df.dtypes):
        if c==object:
            cat_data.append(df.iloc[:,i])
        else:
            num_data.append(df.iloc[:,i])
    cat_data=pd.DataFrame(cat_data).transpose() 
    num_data=pd.DataFrame(num_data).transpose()
    # Remplacer les valeurs catégoriques par des valeurs numériques
    le=LabelEncoder()
    for i in cat_data:
        cat_data[i]=le.fit_transform(cat_data[i])
    df=pd.concat([cat_data,num_data],axis=1)
    return df


def TrainigModelFraud(df):
    df = Preprocessing(df)
    X = df[['amt','category','hours','dob','month','gender','unix_time', 'year','day','city_pop']]
    y = df['is_fraud']
    sss=StratifiedShuffleSplit(n_splits=5,test_size=0.3,random_state=0)
    for train,test in sss.split(X,y):
        X_train,X_test=X.iloc[train],X.iloc[test]
        y_train,y_test=y.iloc[train],y.iloc[test]
    RandomForest = make_pipeline(RandomForestClassifier(random_state=0))
    RandomForest.fit(X_train, y_train)
    ypred = RandomForest.predict(X_test)
    # Save to file 
    pkl_filename = "pickle_modelFraud.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(RandomForest, file)

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
    # separer les données catégorique et numérique
    cat_data=[]
    num_data=[]
    for i,c in enumerate(df.dtypes):
        if c==object:
            cat_data.append(df.iloc[:,i])
        else:
            num_data.append(df.iloc[:,i])
    cat_data=pd.DataFrame(cat_data).transpose() 
    num_data=pd.DataFrame(num_data).transpose()
    # Remplacer les valeurs catégoriques par des valeurs numériques
    le=LabelEncoder()
    for i in cat_data:
        cat_data[i]=le.fit_transform(cat_data[i])
    df=pd.concat([cat_data,num_data],axis=1)
    return df
    
def TrainigModelCateg(df):
    df = PreprocessingCateg(df)
    X = df[['hours','amt','dob','merchant','is_fraud']]
    y = df['category']
    sss=StratifiedShuffleSplit(n_splits=5,test_size=0.3,random_state=0)
    for train,test in sss.split(X,y):
        X_train,X_test=X.iloc[train],X.iloc[test]
        y_train,y_test=y.iloc[train],y.iloc[test]
    DecisionTree = make_pipeline(DecisionTreeClassifier(random_state=0))
    DecisionTree.fit(X_train, y_train)
    ypred = DecisionTree.predict(X_test)
    # Save to file 
    pkl_filename = "pickle_modelCateg.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(DecisionTree, file)   
    

