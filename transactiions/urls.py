
from django.urls import path
from transactiions.views import * 


urlpatterns = [
    path('transactions/', ListeTransactions, name="transactions"),
   

   
]
