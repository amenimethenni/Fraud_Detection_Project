import pandas as pd
import csv
import mysql.connector


df = pd.read_csv('C:/fraudTest.csv')

def Preprocessing(df):
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
    df = df.drop('cc_num', axis=1)
    df = df.drop('street', axis=1)
    df = df.drop('state', axis=1)
    df = df.drop('zip', axis=1)
    df = df.drop('lat', axis=1)
    df = df.drop('long', axis=1)
    df = df.drop('job', axis=1)
    df = df.drop('trans_num', axis=1)
    df = df.drop('merch_lat', axis=1)
    df = df.drop('merch_long', axis=1)
    df = df.drop('minutes', axis=1)
    df = df.drop('secondes', axis=1)
    df['category'] = df['category'].replace(['grocery_pos'],'grocery')
    df['category'] = df['category'].replace(['grocery_net'],'grocery')
    df['category'] = df['category'].replace(['misc_pos'],'misc')
    df['category'] = df['category'].replace(['misc_net'],'misc')
    df['category'] = df['category'].replace(['shopping_pos'],'shopping')
    df['category'] = df['category'].replace(['shopping_net'],'shopping')
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
all_value = []
query = "INSERT INTO  frauddetection.transactions_transaction(amt,category,hours,dob,month,gender,unix_time, year,day,city_pop,merchant,is_fraud)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for row in new_df.itertuples():    
    amt = row.amt
    category = row.category
    hours = row.hours
    dob = row.dob
    month = row.month
    gender = row.gender
    unix_time = row.unix_time
    year = row.year
    day = row.day
    city_pop = row.city_pop
    merchant = row.merchant
    is_fraud = row.is_fraud
    value = (amt,category,hours,dob,month,gender,unix_time, year,day,city_pop,merchant,is_fraud) 
    all_value.append(value)    
cursor.executemany(query, all_value)
conn.commit()





