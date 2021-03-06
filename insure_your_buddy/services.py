from insure_your_buddy.forms import ServiceFilterForm
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.contrib.sessions.backends.db import SessionStore
from django.http.request import QueryDict
from .models import InsuranceService, Customer
from django.contrib.auth import get_user_model
from django.core.paginator import Page, Paginator
from insure_your_buddy.documents import InsuranceServiceDocument
from elasticsearch_dsl import Q
from django.db.models import F
from insurance.utils import get_mongo_client


def create_response(customer_data: Dict[str, Any], service_id: int) -> None:
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
    update_response_counter(service_id)
    desired_services_ids = [
        service.id for service in customer.desired_service.all()
    ]
    if service_id not in desired_services_ids:
        customer.desired_service.add(service_id)


def create_service(service_data: Dict[str, Any], user_id: int) -> None:
    """

    Функция для создания объекта страховой услуги

    """
    company = get_user_model().objects.get(pk=user_id)
    new_service = InsuranceService(
        category=service_data['category'],
        minimal_payment=service_data['minimal_payment'],
        term=service_data['term'],
        company=company,
        description=service_data['description']
    )
    new_service.save()

    db = get_mongo_client()
    service_collection = db['service']
    service = {
        'service_id': new_service.id,
        'view_counter': 0,
        'response_counter': 0
    }
    service_collection.insert_one(service)


def get_sorted_services(request_GET: QueryDict, session: SessionStore, services: QuerySet, **kwargs: Any) -> QuerySet:
    """

    Функция сортировки

    """
    order_by = request_GET.get('sort_by')
    if 'order_by' not in session:
        session['order_by'] = ''
    order_from_session = session['order_by']
    if 'company' in kwargs:
        services = services.filter(company=kwargs['company'])
    if order_by:
        if order_by == order_from_session:
            session['order_by'] = ''
            return services.order_by(order_by).reverse()
        session['order_by'] = order_by
        return services.order_by(order_by)
    else:
        return services.order_by('-id')


def filters_to_session(session: SessionStore, form: ServiceFilterForm) -> None:
    """

    Функция записи параметров фильтрации в сессию

    """
    if 'filters' not in session:
        session['filters'] = {}
    filters = session['filters']
    filter_data = form.cleaned_data
    for key, value in filter_data.items():
        filters[key] = value
    session['filter'] = filters


def category_filter(filters: Dict[str, str], services: QuerySet) -> QuerySet:
    """

    Фильтр по категории

    """
    if 'category' in filters and filters['category'] != '0':
        services = services.filter(category=int(filters['category']))
    return services


def minimal_payment_filter(filters: Dict[str, str], services: QuerySet) -> QuerySet:
    """

    Фильтр по минимальной стоимости

    """
    if 'minimal_payment' in filters and filters['minimal_payment'] != '0':
        min_val, max_val = filters['minimal_payment'].split(' ')
        min_val, max_val = int(min_val), int(max_val)
        services = services.filter(minimal_payment__range=(min_val, max_val))
    return services


def term_filter(filters: Dict[str, str], services: QuerySet) -> QuerySet:
    """

    Фильтр по сроку страхования

    """
    if 'term' in filters and filters['term'] != '0':
        min_val, max_val = filters['term'].split(' ')
        min_val, max_val = int(min_val), int(max_val)
        services = services.filter(term__range=(min_val, max_val))
    return services


def company_filter(filters: Dict[str, str], services: QuerySet) -> QuerySet:
    """

    Фильтр по компании

    """
    if 'company' in filters and filters['company'] != '0':
        services = services.filter(company=filters['company'])
    return services


def get_filtered_services(session: SessionStore, services: QuerySet) -> QuerySet:
    """

    Функция для применения всех фильтров

    """
    if 'filters' in session:
        filters = session['filters']
        services = category_filter(filters, services)
        services = minimal_payment_filter(filters, services)
        services = term_filter(filters, services)
        services = company_filter(filters, services)
    return services


def get_paginated_objects(request_GET: QueryDict, objects: QuerySet) -> Page:
    """

    Функция для пагинации

    """
    paginator = Paginator(objects, 5)
    page_number = request_GET.get('p')
    objects = paginator.get_page(page_number)
    return objects


def search_service(search_data: str) -> QuerySet:
    """

    Функция поиска

    """
    search = InsuranceServiceDocument.search()
    category_q = Q('fuzzy', category=search_data)
    company_q = Q('fuzzy', company__company_name=search_data)
    description_q = Q('fuzzy', description=search_data)
    service_title_q = Q('fuzzy', service_title=search_data)
    query = category_q | company_q | description_q | service_title_q
    search_result = search.query(query)
    return search_result.to_queryset()


def update_response_counter(service_id: int) -> None:
    db = get_mongo_client()
    service_collection = db['service']

    service_collection.update_one(
        {'service_id': service_id},
        {'$inc': {'response_counter': 1}}
    )


def update_view_counter(service_id: int) -> None:
    db = get_mongo_client()
    service_collection = db['service']

    service_collection.update_one(
        {'service_id': service_id},
        {'$inc': {'view_counter': 1}}
    )
