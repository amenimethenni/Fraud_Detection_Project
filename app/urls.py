
from django.urls import path, re_path
from app import views # import de fich view qui existe dans app


#Liste des urls
urlpatterns = [


    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

 




]
