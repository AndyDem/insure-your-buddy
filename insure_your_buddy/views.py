from typing import Any, Dict
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from .services import (
    create_response,
    create_service,
    get_filtered_services,
    get_paginated_objects,
    get_sorted_services,
    filters_to_session,
    search_service,
    update_view_counter
)
from .tasks import send_customer_data
from .forms import (
    InsuranceServiceForm,
    CustomerResponseForm,
    ServiceFilterForm,
    SearchForm
)
from .models import (
    InsuranceService,
    Customer
)
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalDeleteView,
    BSModalFormView,
    BSModalReadView
)


class MainView(generic.FormView):
    """

    View для отображения главной страницы с фильтруемыми страховыми услугами

    """
    template_name = 'insure_your_buddy/main.html'
    form_class = SearchForm
    success_url = reverse_lazy('insure_your_buddy:search_results')

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        request_GET = self.request.GET
        session = self.request.session
        services = InsuranceService.objects.all()
        services = get_sorted_services(request_GET, session, services)
        services = get_filtered_services(session, services)
        services = get_paginated_objects(request_GET, services)

        context = {
            'services': services,
            'form': self.form_class()
        }

        return context

    def form_valid(self, form) -> HttpResponse:
        self.request.session['search'] = form.cleaned_data['search']
        return super().form_valid(form)


class SearchResultsView(MainView):
    """

    View для отображения результатов поиска

    """
    template_name = 'insure_your_buddy/search_results.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        request_GET = self.request.GET
        session = self.request.session
        services = search_service(session['search'])
        services = get_sorted_services(request_GET, session, services)
        services = get_filtered_services(session, services)
        services = get_paginated_objects(request_GET, services)
        context = {
            'services': services,
            'form': self.form_class()
        }
        return context


class ProfileView(generic.TemplateView):
    """

    View личного кабинета с фильтруемыми
    страховыми услугами конкретной компании

    """
    template_name = 'insure_your_buddy/profile.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        request_GET = self.request.GET
        session = self.request.session
        services = InsuranceService.objects.all()
        services = get_sorted_services(
            request_GET=request_GET,
            session=session,
            services=services,
            company=self.request.user.id
        )
        services = get_filtered_services(session, services)
        services = get_paginated_objects(request_GET, services)

        context = {'services': services}
        return context


class ServiceDetailView(BSModalReadView):
    """

    View страницы услуги

    """

    model = InsuranceService
    template_name = 'insure_your_buddy/detail.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        request_GET = self.request.GET
        service_id = self.kwargs['pk']
        customers = Customer.objects.filter(desired_service__id=service_id)
        customers = customers.order_by('-id')
        customers = get_paginated_objects(request_GET, customers)
        context = {
            'customers': customers,
            'service': super().get_object()
        }
        if self.request.user.is_anonymous:
            update_view_counter(service_id)
        return context


class FilterServiceView(BSModalFormView):
    """

    View фильтрации по категории

    """

    form_class = ServiceFilterForm
    template_name = 'insure_your_buddy/filter.html'

    def get_form(self) -> ServiceFilterForm:
        if self.request.META.get('HTTP_REFERER').endswith('profile/'):
            form = ServiceFilterForm(**self.get_form_kwargs())
            form.fields.pop('company')
            return form
        else:
            return super().get_form()

    def form_valid(self, form) -> HttpResponse:
        session = self.request.session
        filters_to_session(session, form)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.request.META.get('HTTP_REFERER')


class CustomerResponseView(BSModalCreateView):
    """

    View создания отклика(заявки) и отправки на почту компании

    """

    form_class = CustomerResponseForm
    template_name = 'insure_your_buddy/response.html'
    success_message = 'Success'
    success_url = reverse_lazy('insure_your_buddy:main')

    def form_valid(self, form) -> HttpResponse:
        if not self.request.is_ajax():
            customer_data = form.cleaned_data
            create_response(
                customer_data=customer_data,
                service_id=self.kwargs['service_id']
            )
            send_customer_data.delay(
                customer_data=customer_data,
                service_id=self.kwargs['service_id']
            )
        return redirect(self.success_url)


class CreateServiceView(BSModalCreateView):
    """

    View создания страховой услуги

    """

    form_class = InsuranceServiceForm
    template_name = 'insure_your_buddy/create_service.html'
    success_message = 'Success'
    success_url = reverse_lazy('insure_your_buddy:profile')

    def form_valid(self, form) -> HttpResponse:
        if not self.request.is_ajax():
            service_data = form.cleaned_data
            user_id = self.request.user.id
            create_service(service_data, user_id)
        return redirect(self.success_url)


class UpdateServiceView(BSModalUpdateView):
    """

    View для изменения страховой услуги
    Временно отключен

    """

    model = InsuranceService
    form_class = InsuranceServiceForm
    template_name = 'insure_your_buddy/update_service.html'
    success_message = 'Success'
    success_url = reverse_lazy('insure_your_buddy:profile')


class DeleteServiceView(BSModalDeleteView):
    """

    View для удаления страховой услуги

    """

    model = InsuranceService
    template_name = 'insure_your_buddy/delete_service.html'
    success_message = 'Success'
    success_url = reverse_lazy('insure_your_buddy:profile')
