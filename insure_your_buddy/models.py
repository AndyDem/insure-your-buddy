from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()


class InsuranceService(models.Model):
    category = models.CharField(max_length=100)
    percentage_rate = models.IntegerField()
    term = models.IntegerField()
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=600)
