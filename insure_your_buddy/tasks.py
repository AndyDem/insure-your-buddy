from .models import InsuranceService
from .services import get_service_title
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_customer_data(customer_data, service_id):
    """

    Функция для отправки письма с данными нового потребителя
    в страховую компанию

    """
    title = get_service_title(service_id)
    company_mail = InsuranceService.objects.get(pk=service_id).company.email
    return send_mail(
        subject='New customer response',
        message=f'You have new customer on "{title}"!\n\
            Customer is {customer_data["full_name"]},\
                phone number is {customer_data["phone_number"]}\
                    and email is {customer_data["email"]}',
        from_email='InsureYourBuddy <insure_your_buddy@support.com>',
        recipient_list=[company_mail]
    )
