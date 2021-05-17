
from django.urls import path
from comptess.views import * 


urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path ('listetransactFraud/',listetransactFraud,name="listetransactFraud")
   

   
]
