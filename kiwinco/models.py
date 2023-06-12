from typing import Any
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CartedItem(models.Model):
    def getDisplayPrice(self):
        return "{0:.2f}".format(self.price/100)
    
    itemId = models.PositiveIntegerField()
    itemName = models.CharField(max_length=30)
    buyerId = models.PositiveIntegerField()
    itemSize = models.CharField(max_length=3)
    price = models.IntegerField(default=0)

class Item(models.Model):

    def getDisplayPrice(self):
        return "{0:.2f}".format(self.Price/100)

    ItemName = models.CharField(max_length=30)
    Description = models.CharField(max_length=200)
    Price = models.IntegerField(default=0)
    PriceFloat = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    Stock_XS = models.IntegerField(default=0)
    Stock_S = models.IntegerField(default=0)
    Stock_M = models.IntegerField(default=0)
    Stock_L = models.IntegerField(default=0)
    Stock_XL = models.IntegerField(default=0)
    Featured = models.BooleanField()
    Jumper_Jacket = models.BooleanField()
    Shirt = models.BooleanField()
    Pants = models.BooleanField()
    Image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.ItemName
    

class Purchase(models.Model):
    itemName = models.CharField(max_length=30)
    itemSize = models.CharField(max_length=3)
    buyerId = models.PositiveIntegerField()
    Price = models.IntegerField(default=0)
    orderID = models.CharField(primary_key=True, max_length=100, default=uuid.uuid4,unique=True, editable=False)
    
    def __str__(self):
        return self.orderID
    

    

  