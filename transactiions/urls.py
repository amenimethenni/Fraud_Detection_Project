
from django.urls import path
from transactiions.views import * 
from transactiions import views


urlpatterns = [
    path('transactions/', ListeTransactions, name="transactions"),
    path('fraudupdate/',fraudupdate, name='fraudupdate')

   

   
]
