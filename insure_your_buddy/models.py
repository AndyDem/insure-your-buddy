from django.db import models
from django.contrib.auth.models import User


class InsuranceService(models.Model):
    VEHICLE = 1
    HOME_INSURANCE = 2
    LIFE = 3
    PROPERTY = 4
    COMBO = 5
    CATEGORIES = (
        (VEHICLE, 'Vehicle'),
        (HOME_INSURANCE, 'Home insurance'),
        (LIFE, 'Life'),
        (PROPERTY, 'Property'),
        (COMBO, 'Combo')
    )

    category = models.PositiveSmallIntegerField(choices=CATEGORIES)
    minimal_payment = models.IntegerField()
    term = models.IntegerField()
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=600)


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    desired_service = models.ManyToManyField(InsuranceService)
