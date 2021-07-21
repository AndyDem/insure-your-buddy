from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import (
    InsuranceServiceForm,
    CustomerForm,
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


def MainView(request):
    if InsuranceServices:
        context = {'services': InsuranceServices}
    else:
        context = {}
    return render(request, 'insure_your_buddy/main.html', context)


def InsuranceServices():
    services = InsuranceService.objects.filter()
    return services


class ServiceFilterView(BSModalFormView):
    template_name = 'insure_your_buddy/filter.html'
    form_class = ServiceFilterForm

    def form_valid(self, form):
        self.filter = '?type=' + form.cleaned_data['type']
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('main') + self.filter


class CustomSignupView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'insure_your_buddy/login-signup.html'
    success_message = 'Success'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Sign up'
        return context


class CustomLoginView(BSModalLoginView):
    form_class = CustomAuthenticationForm
    template_name = 'insure_your_buddy/login-signup.html'
    success_message = 'Success'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Log in'
        return context


class CreateServiceView(BSModalCreateView):
    form_class = InsuranceServiceForm
    template_name = 'insure_your_buddy/create_service.html'
    success_message = 'Success'
    success_url = reverse_lazy('account')


class UpdateServiceView(BSModalUpdateView):
    model = InsuranceService
    form_class = InsuranceServiceForm
    template_name = 'insure_your_buddy/update_service.html'
    success_message = 'Success'
    success_url = reverse_lazy('account')


class DeleteServiceView(BSModalDeleteView):
    model = InsuranceService
    template_name = 'insure_your_buddy/delete_service.html'
    success_message = 'Success'
    success_url = reverse_lazy('account')
