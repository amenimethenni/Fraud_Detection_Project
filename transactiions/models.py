from django.db import models
from django.contrib.auth.models import User

from Cartes_Creditss.models import credit_card
# Create your models here.

class Transactiions(models.Model):

    CarteCredit= models.ForeignKey(credit_card, on_delete=models.CASCADE,null=True)

    merchant = models.CharField(max_length = 100)
    category = models.CharField(max_length = 100, null=True )
    amt = models.FloatField(null=True)
    gender = models.CharField(max_length = 100, null=True )
    city_pop = models.IntegerField(null=True)
    dob =  models.CharField(max_length = 100, null=True )
    unix_time =  models.IntegerField(null=True)
    is_fraud =  models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    hours = models.IntegerField(null=True)

    category_pred = models.CharField(max_length = 100, null=True )
    is_fraud_pred = models.IntegerField(null=True)
    #liste_etats= (('En traitement' , 'En traitement'), ('Traitée' , 'Traitée'))
    #etat = models.CharField(max_length = 100, null=True , choices = liste_etats )
    #Status = models.CharField(max_length = 100, null=True )
