from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
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
            'minimal_payment',
            'term',
            'description'
        ]


class CustomerResponseForm(BSModalModelForm):
    class Meta:
        model = Customer
        fields = [
            'full_name',
            'phone_number',
            'email'
        ]


class ServiceFilterForm(BSModalForm):
    NO_FILTER = 0
    choices = ((NO_FILTER, 'All'),) + InsuranceService.CATEGORIES
    category = forms.ChoiceField(choices=choices)
