
from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from transactiions.views import * 
from comptess.views import *


from authentication.views import *


urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('transactions/', ListeTransactions, name="transactions"),


    path('users/', users, name="users"),
    path('dashboard/', dashboard, name="dashboard"),
    path('listetransactFraud/',listetransactFraud,name ="listetransactFraud"),
    path('getlisteuser/',getlisteuser,name ="getlisteuser"),
    path('getuser/',getuser,name ="getuser"),
    path('statistique/',admin,name ="admin"),
    




   
]
