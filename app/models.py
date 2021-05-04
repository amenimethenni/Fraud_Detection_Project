from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amt = models.FloatField(null=True)
    category = models.CharField(max_length = 100, null=True )
    hours = models.IntegerField()
    dob =  models.DateField(null=True)
    month = models.IntegerField()
    gender = models.CharField(max_length = 100, null=True )
    unix_time =  models.FloatField(null=True)
    year = models.IntegerField()
    day = models.IntegerField()
    city_pop = models.CharField(max_length = 100 , null=True)
    merchant = models.CharField(max_length = 100)
    is_fraud =  models.IntegerField()
    category_pred = models.CharField(max_length = 100, null=True )
    is_fraud_pred = models.IntegerField()
    liste_etats= (('En cours' , 'En cours'),('En traitement' , 'En traitement'), ('Traitée' , 'Traitée'))
    etat = models.CharField(max_length = 100, null=True , choices = liste_etats )



