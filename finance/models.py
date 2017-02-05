from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class user(models.Model):
    user = models.OneToOneField(User)
    cash = models.DecimalField(max_digits=10, decimal_places=2)

class transactionTable(models.Model):
    user = models.ForeignKey(User)
    symbol = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    shares = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    trnDateTime = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return self.symbol + ' ' + str((self.trnDateTime).day) + ' ' +  str((self.trnDateTime).hour)
