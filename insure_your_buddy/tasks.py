from celery import shared_task
from django.core.mail import send_mail
from .models import *


@shared_task
def send_customer_data(customer_data, service_id, to_mail):
    """

    Функция для отправки письма с данными нового потребителя
    в страховую компанию

    """
    return send_mail(
        subject='New customer response',
        message=f'You have new customer on insurance service {service_id}!\n\
            Customer is {customer_data["full_name"]},\
                phone number is {customer_data["phone_number"]}\
                    and email is {customer_data["email"]}',
        from_email='InsureYourBuddy <insure_your_buddy@support.com>',
        recipient_list=[to_mail]
    )
