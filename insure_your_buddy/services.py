from .models import InsuranceService, Customer
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator


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
    service = InsuranceService.objects.get(pk=service_id)
    if service not in customer.desired_service.all():
        customer.desired_service.add(service_id)
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


def get_service_title(service_id):
    """

    Функция получения названия услуги

    """
    service = InsuranceService.objects.get(pk=service_id)
    term = 'months' if service.term > 1 else 'month'
    title = f'{ service.get_category_display() } insurance\
         with minimal payment of { service.minimal_payment }$ \
             for { service.term } {term}.'
    return title


def get_sorted_services(request, **kwargs):
    """

    Функция сортировки

    """
    order_by = request.GET.get('sort_by')
    if 'order_by' not in request.session:
        request.session['order_by'] = ''
    order_from_session = request.session['order_by']
    services = InsuranceService.objects.all()
    if 'company' in kwargs:
        services = services.filter(company=kwargs['company'])
    if order_by:
        if order_by == order_from_session:
            request.session['order_by'] = ''
            return services.order_by(order_by).reverse()
        request.session['order_by'] = order_by
        return services.order_by(order_by)
    else:
        return services.order_by('-id')


def filters_to_session(request, form):
    """

    Функция записи параметров фильтрации в сессию

    """
    if 'filters' not in request.session:
        request.session['filters'] = {}
    filters = request.session['filters']
    filter_data = form.cleaned_data
    for key, value in filter_data.items():
        filters[key] = value
    request.session['filter'] = filters


def category_filter(filters, services):
    """

    Фильтр по категории

    """
    if 'category' in filters and filters['category'] != '0':
        services = services.filter(category=int(filters['category']))
    return services


def minimal_payment_filter(filters, services):
    """

    Фильтр по минимальной стоимости

    """
    if 'minimal_payment' in filters and filters['minimal_payment'] != '0':
        min_val, max_val = filters['minimal_payment'].split(' ')
        min_val, max_val = int(min_val), int(max_val)
        services = services.filter(minimal_payment__range=(min_val, max_val))
    return services


def term_filter(filters, services):
    """

    Фильтр по сроку страхования

    """
    if 'term' in filters and filters['term'] != '0':
        min_val, max_val = filters['term'].split(' ')
        min_val, max_val = int(min_val), int(max_val)
        services = services.filter(term__range=(min_val, max_val))
    return services


def company_filter(filters, services):
    """

    Фильтр по компании

    """
    if 'company' in filters and filters['company'] != '0':
        services = services.filter(company=filters['company'])
    return services


def get_filtered_services(request, services):
    """

    Функция для применения всех фильтров

    """
    if 'filters' in request.session:
        filters = request.session['filters']
        services = category_filter(filters, services)
        services = minimal_payment_filter(filters, services)
        services = term_filter(filters, services)
        services = company_filter(filters, services)
    return services


def get_paginated_objects(request, objects):
    """

    Функция для пагинации

    """
    paginator = Paginator(objects, 5)
    page_number = request.GET.get('p')
    objects = paginator.get_page(page_number)
    return objects
