from django.core import paginator
from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .services import create_response, create_service
from .tasks import send_customer_data
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
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

    services = InsuranceService.objects.all()

    if 'filter' in request.session:
        if int(request.session['filter']) == 0:
            services = services
        else:
            services = services.filter(category=int(
                request.session['filter']))

    paginator = Paginator(services, 5)
    page_number = request.GET.get('p')
    services = paginator.get_page(page_number)

    context = {
        'services': services
    }

    return render(request, 'insure_your_buddy/main.html', context)


def profile_view(request):
    """

    View личного кабинета с фильтруемыми
    страховыми услугами конкретной компании

    """

    if request.user.is_anonymous:
        return redirect('insure_your_buddy:main')

    services = InsuranceService.objects.filter(company=request.user.id)

    if 'filter' in request.session:
        if int(request.session['filter']) == 0:
            services = services
        else:
            services = services.filter(category=int(request.session['filter']))

    paginator = Paginator(services, 5)
    page_number = request.GET.get('p')
    services = paginator.get_page(page_number)

    context = {
        'services': services
    }
    return render(request, 'insure_your_buddy/profile.html', context)


def show_responses_view(request, service_id):
    """

    View для отображения откликов(заявок) на конкретную услугу

    """

    service = InsuranceService.objects.get(pk=service_id)
    term = 'months' if service.term > 1 else 'month'
    title = f'{ service.get_category_display() } insurance\
         with minimal payment of { service.minimal_payment }$ \
             for { service.term } {term}.'
    customers = Customer.objects.filter(desired_service__id=service_id)
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

    def form_valid(self, form):
        self.request.session['filter'] = form.cleaned_data['category']
        print(self.request.META.get('HTTP_REFERER'))
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
            company_mail = InsuranceService.objects.get(
                pk=self.kwargs['service_id']).company.email
            send_customer_data.delay(
                cusromer_data=customer_data,
                service_id=self.kwargs['service_id'],
                to_mail=company_mail
            )
            return redirect(self.success_url)
        else:
            return super().form_invalid(form)


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
        else:
            return super().form_invalid(form)


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
