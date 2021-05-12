import pandas as pd
import csv
import mysql.connector
import random

df = pd.read_csv('C:/fraudTest.csv')


def Preprocessing(df):
    df = df.drop('last',axis=1)
    df = df.drop('first',axis=1)
    df = df.drop('city',axis=1)
    df = df.drop('Unnamed: 0', axis=1)  
    df = df.drop('street', axis=1)
    df = df.drop('state', axis=1)
    df = df.drop('zip', axis=1)
    df = df.drop('lat', axis=1)
    df = df.drop('long', axis=1)
    df = df.drop('job', axis=1)
    df = df.drop('trans_num', axis=1)
    df = df.drop('merch_lat', axis=1)
    df = df.drop('merch_long', axis=1)
    df = df.drop('merchant', axis=1)
    df = df.drop('category', axis=1)
    df = df.drop('amt', axis=1)
    df = df.drop('gender', axis=1)
    df = df.drop('city_pop', axis=1)
    df = df.drop('dob', axis=1)
    df = df.drop('unix_time', axis=1)
    df = df.drop('is_fraud', axis=1)
    df = df.drop('trans_date_trans_time',axis=1)
    df = df.rename(columns={"cc_num": "num_Carte_Credit"})
    return df
new_df = Preprocessing(df)
print(new_df.info())
print (new_df.head(10))


# connect to database
conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="frauddetection"
)
cursor = conn.cursor()

# creating column list for insertion
cols = "`,`".join([str(i) for i in new_df.columns.tolist()])

# Insert DataFrame recrds one by one.
for i,row in new_df.iterrows():
    sql = "INSERT INTO `cartes_creditss_credit_card` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))

# the connection is not autocommitted by default, so we must commit to save our changes
connection.commit()






