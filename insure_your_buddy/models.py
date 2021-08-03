from django.db import models
from django.contrib.auth import get_user_model


class InsuranceService(models.Model):
    """
    
    Модель страховой услуги
    
    """
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
    minimal_payment = models.PositiveIntegerField()
    term = models.PositiveIntegerField()
    company = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField()
    customers_count = models.PositiveIntegerField(default=0)


    def get_service_title(self):
        """

        Функция получения названия услуги

        """
        term = 'months' if self.term > 1 else 'month'
        title = f'{ self.get_category_display() } insurance\
            with minimal payment of { self.minimal_payment }$ \
                for { self.term } {term}.'
        return title

class Customer(models.Model):
    """
    
    Модель отклика потребителя
    
    """
    full_name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    desired_service = models.ManyToManyField(InsuranceService)
