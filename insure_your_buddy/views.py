from insure_your_buddy.documents import InsuranceServiceDocument
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .services import (
    create_response,
    create_service,
    get_filtered_services,
    get_paginated_objects,
    get_sorted_services,
    filters_to_session
)
from .tasks import send_customer_data
from .forms import (
    InsuranceServiceForm,
    CustomerResponseForm,
    ServiceFilterForm
)
from .models import (
    InsuranceService,
    Customer
)
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalDeleteView,
    BSModalFormView
)


def main_view(request):
    """

    View для отображения главной страницы с фильтруемыми страховыми услугами

    """
    services = get_sorted_services(request)
    services = get_filtered_services(request, services)
    services = get_paginated_objects(request, services)

    s = InsuranceServiceDocument.search()
    s = s.filter('term', company='insurance-company 2')
    s = s.to_queryset()
    for hit in s:
        print(
            f"{type(hit)}{hit}"
        )
    

    context = {'services': services}

    return render(request, 'insure_your_buddy/main.html', context)


def profile_view(request):
    """

    View личного кабинета с фильтруемыми
    страховыми услугами конкретной компании

    """
    if request.user.is_anonymous:
        return redirect('insure_your_buddy:main')

    services = get_sorted_services(request, company=request.user.id)
    services = get_filtered_services(request, services)
    services = get_paginated_objects(request, services)

    context = {'services': services}

    return render(request, 'insure_your_buddy/profile.html', context)


def show_responses_view(request, service_id):
    """

    View для отображения откликов(заявок) на конкретную услугу

    """
    customers = Customer.objects.filter(desired_service__id=service_id)
    customers = customers.order_by('-id')
    customers = get_paginated_objects(request, customers)
    
    title = InsuranceService.objects.get(pk=service_id).get_service_title()

    context = {
        'title': title,
        'customers': customers
    }

    return render(request, 'insure_your_buddy/show_responses.html', context)


class FilterServiceView(BSModalFormView):
    """

    View фильтрации по категории

    """

    form_class = ServiceFilterForm
    template_name = 'insure_your_buddy/filter.html'

    def get_form(self):
        if self.request.META.get('HTTP_REFERER').endswith('profile/'):
            form = ServiceFilterForm(**self.get_form_kwargs())
            form.fields.pop('company')
            return form
        else:
            return super().get_form()

    def form_valid(self, form):
        filters_to_session(self.request, form)
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class CustomerResponseView(BSModalCreateView):
    """

    View создания отклика(заявки) и отправки на почту компании

    """

    form_class = CustomerResponseForm
    template_name = 'insure_your_buddy/response.html'
    success_message = 'Success'
    success_url = reverse_lazy('insure_your_buddy:main')

    def form_valid(self, form):
        if not self.request.is_ajax():
            customer_data = form.cleaned_data
            create_response(customer_data, self.kwargs['service_id'])
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

    def form_valid(self, form):
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
    success_url = reverse_lazy('profile')


class DeleteServiceView(BSModalDeleteView):
    """

    View для удаления страховой услуги

    """

    model = InsuranceService
    template_name = 'insure_your_buddy/delete_service.html'
    success_message = 'Success'
    success_url = reverse_lazy('insure_your_buddy:profile')
