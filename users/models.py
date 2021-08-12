from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    
    Модель пользователя (компании)
    
    """
    company_name = models.CharField(max_length=300)

    def __str__(self):
        return self.company_name