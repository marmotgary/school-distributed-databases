from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Account(User):
    address = models.CharField(max_length=128)
    country = models.CharField(max_length=64)
    post_code = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)

class Order(models.Model):
    user = models.ForeignKey(Account)
    ordered_date = models.DateField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=128)

class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000, default="Description")
    category = models.ForeignKey(Category)
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    brand = models.CharField(max_length=128, blank=True)
    color = models.CharField(max_length=32, blank=True)
