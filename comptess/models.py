from django.db import models

from django.db import models
from django.contrib.auth.models import User
#from Cartes_Creditss.models import credit_card


# Create your models here.

class Account(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #CarteCredit= models.OneToOneField(credit_card, on_delete=models.CASCADE)

    num_compte = models.IntegerField(null=True)
    date_ouverture = models.DateTimeField(null=True)
    solde = models.FloatField(null=True)
    liste_types_compte= (('compte courant ' ,'compte courant '), ('compte d’épargne' , 'compte d’épargne'))
    type_compte = models.CharField(max_length = 100, null=True , choices = liste_types_compte )
    
