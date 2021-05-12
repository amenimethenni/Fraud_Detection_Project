from django.db import models
from comptess.models import Account



class credit_card(models.Model):
    compte = models.OneToOneField(Account, on_delete=models.CASCADE,null=True)
    num_Carte_Credit= models.CharField(primary_key=True , max_length=100)
    date_expiration = models.DateTimeField(null=True)
    liste_types_cartes= (('carte Visa' ,'carte Visa'), ('carte MasterCard' , 'carte MasterCard'))
    type_carte = models.CharField(max_length = 100, null=True ,choices = liste_types_cartes)
    