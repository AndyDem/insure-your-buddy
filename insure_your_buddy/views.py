from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import (
    InsuranceServiceForm,
    CustomerResponseForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    ServiceFilterForm
)
from .models import (
    InsuranceService,
    Customer
)
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
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
            services = services.filter(category=int(request.session['filter']))

    context = {'services': services}

    return render(request, 'insure_your_buddy/main.html', context)


def profile_view(request):
    """

    View личного кабинета с фильтруемыми страховыми услугами конкретной компании

    """

    if '_auth_user_id' not in request.session:
        return redirect('main')

    company = User.objects.get(pk=int(request.session['_auth_user_id']))
    services = InsuranceService.objects.filter(company=company)

    if 'filter' in request.session:
        if int(request.session['filter']) == 0:
            services = services
        else:
            services = services.filter(category=int(request.session['filter']))

    context = {
        'services': services
    }
    return render(request, 'insure_your_buddy/profile.html', context)


def show_responses_view(request, service_id):
    """

    View для отображения откликов(заявок) на конкретную услугу

    """

    services = InsuranceService.objects.filter(pk=service_id)
    customers = Customer.objects.filter(desired_service__id=service_id)
    context = {
        'services': services,
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

    View создания отклика(заявки)

    """

    form_class = CustomerResponseForm
    template_name = 'insure_your_buddy/response.html'
    success_message = 'Success'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        if not self.request.is_ajax():
            customer_data = form.cleaned_data
            if Customer.objects.filter(
                full_name=customer_data['full_name'],
                phone_number=customer_data['phone_number'],
                email=customer_data['email']
            ):
                Customer.objects.get(
                    full_name=customer_data['full_name'],
                    phone_number=customer_data['phone_number'],
                    email=customer_data['email']
                ).desired_service.add(self.kwargs['service_id'])
            else:
                Customer.objects.create(
                    full_name=customer_data['full_name'],
                    phone_number=customer_data['phone_number'],
                    email=customer_data['email']
                ).desired_service.add(self.kwargs['service_id'])
            service = InsuranceService.objects.get(
                pk=self.kwargs['service_id'])
            service.customers_count += 1
            service.save()
            return redirect('main')
        else:
            return redirect('main')


class CustomSignupView(BSModalCreateView):
    """

    View регистрации пользователя

    """

    form_class = CustomUserCreationForm
    template_name = 'insure_your_buddy/login-signup.html'
    success_message = 'Success'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Sign up'
        return context


class CustomLoginView(BSModalLoginView):
    """

    View аутентификации

    """

    form_class = CustomAuthenticationForm
    template_name = 'insure_your_buddy/login-signup.html'
    success_message = 'Success'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Log in'
        return context


class CreateServiceView(BSModalCreateView):
    """

    View создания страховой услуги

    """

    form_class = InsuranceServiceForm
    template_name = 'insure_your_buddy/create_service.html'
    success_message = 'Success'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        if not self.request.is_ajax():
            user_id = int(self.request.session['_auth_user_id'])
            company = User.objects.get(pk=user_id)
            InsuranceService.objects.create(
                category=form.cleaned_data['category'],
                minimal_payment=form.cleaned_data['minimal_payment'],
                term=form.cleaned_data['term'],
                company=company,
                description=form.cleaned_data['description']
            )
            return redirect('profile')
        else:
            return redirect('profile')


# class UpdateServiceView(BSModalUpdateView):
#     """

#     View для изменения страховой услуги
#     Временно отключен

#     """

#     model = InsuranceService
#     form_class = InsuranceServiceForm
#     template_name = 'insure_your_buddy/update_service.html'
#     success_message = 'Success'
#     success_url = reverse_lazy('profile')


class DeleteServiceView(BSModalDeleteView):
    """

    View для удаления страховой услуги

    """

    model = InsuranceService
    template_name = 'insure_your_buddy/delete_service.html'
    success_message = 'Success'
    success_url = reverse_lazy('profile')
