from insure_your_buddy.forms import InsuranceServiceForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import InsuranceService, Customer
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalDeleteView
)


def MainView(request):
    if InsuranceServices:
        context = {'services': InsuranceServices}
    else:
        context = {}
    return render(request, 'insure_your_buddy/main.html', context)

def InsuranceServices():
    services = InsuranceService.objects.all()
    return services


class CustomSignupView(BSModalCreateView):
    form_class = UserCreationForm
    template_name = 'insure_your_buddy/signup.html'
    success_message = 'Success'
    success_url = reverse_lazy('account')


class CustomLoginView(BSModalLoginView):
    form_class = AuthenticationForm
    template_name = 'insure_your_buddy/login.html'
    success_message = 'Success'
    success_url = reverse_lazy('account')


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
