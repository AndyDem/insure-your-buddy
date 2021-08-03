from .models import InsuranceService
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_customer_data(customer_data, service_id):
    """

    Функция для отправки письма с данными нового потребителя
    в страховую компанию

    """
    service = InsuranceService.objects.get(pk=service_id)
    title = service.get_service_title()
    company_mail = service.company.email
    return send_mail(
        subject='New customer response',
        message=f'You have new customer on "{title}"!\n\
            Customer is {customer_data["full_name"]},\
                phone number is {customer_data["phone_number"]}\
                    and email is {customer_data["email"]}',
        from_email='InsureYourBuddy <insure_your_buddy@support.com>',
        recipient_list=[company_mail]
    )
