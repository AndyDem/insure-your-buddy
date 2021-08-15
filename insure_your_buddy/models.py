from django.db import models
from django.contrib.auth import get_user_model
from insurance.utils import get_mongo_client


class InsuranceService(models.Model):
    """

    Модель страховой услуги

    """
    VEHICLE = 1
    HOME = 2
    LIFE = 3
    PROPERTY = 4
    COMBO = 5
    CATEGORIES = (
        (VEHICLE, 'Vehicle'),
        (HOME, 'Home'),
        (LIFE, 'Life'),
        (PROPERTY, 'Property'),
        (COMBO, 'Combo')
    )

    category = models.PositiveSmallIntegerField(choices=CATEGORIES)
    minimal_payment = models.PositiveIntegerField()
    term = models.PositiveIntegerField()
    company = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField()

    def get_service_title(self):
        """

        Функция получения названия услуги

        """
        term = 'months' if self.term > 1 else 'month'
        title = f'{ self.get_category_display() } insurance\
            with minimal payment of { self.minimal_payment }$ \
                for { self.term } {term}.'
        return title

    def get_views_counter(self):
        db = get_mongo_client()
        service_collection = db['service']
        service = service_collection.find_one({'service_id': self.id})
        view_counter = service['view_counter']
        return view_counter

    def get_response_counter(self):
        db = get_mongo_client()
        service_collection = db['service']
        service = service_collection.find_one({'service_id': self.id})
        response_counter = service['response_counter']
        return response_counter


class Customer(models.Model):
    """

    Модель отклика потребителя

    """
    full_name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    desired_service = models.ManyToManyField(InsuranceService)
