from .models import InsuranceService, Customer
from django.contrib.auth import get_user_model


def create_response(customer_data, service_id):
    """

    Функция для создания объекта отклика или
    добавления значения в ManyToManyField.
    Дополнительно обновляет счетчик откликов
    у объекта услуги    

    """
    customer, _ = Customer.objects.get_or_create(
        full_name=customer_data['full_name'],
        phone_number=customer_data['phone_number'],
        email=customer_data['email']
    )
    customer.desired_service.add(service_id)
    service = InsuranceService.objects.get(pk=service_id)
    service.customers_count += 1
    service.save()


def create_service(service_data, user_id):
    """

    Функция для создания объекта страховой услуги

    """
    company = get_user_model().objects.get(pk=user_id)
    InsuranceService.objects.create(
        category=service_data['category'],
        minimal_payment=service_data['minimal_payment'],
        term=service_data['term'],
        company=company,
        description=service_data['description']
    )
