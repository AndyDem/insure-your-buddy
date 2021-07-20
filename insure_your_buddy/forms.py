from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import fields
from .models import InsuranceService, Customer
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class CustomAuthenticationForm(PopRequestMixin, CreateUpdateAjaxMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class InsuranceServiceForm (BSModalModelForm):
    class Meta:
        model = InsuranceService
        fields = [
            'category',
            'percentage_rate',
            'term',
            'company',
            'description'
        ]


class CustomerForm(BSModalModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'phone_number',
            'email'
        ]
