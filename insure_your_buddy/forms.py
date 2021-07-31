from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import InsuranceService, Customer


class InsuranceServiceForm (BSModalModelForm):
    """

    Форма для создания объекта страховой услуги

    """
    class Meta:
        model = InsuranceService
        fields = [
            'category',
            'minimal_payment',
            'term',
            'description'
        ]


class CustomerResponseForm(BSModalModelForm):
    """

    Форма для создания объекта отклика потребителя

    """
    class Meta:
        model = Customer
        fields = [
            'full_name',
            'phone_number',
            'email'
        ]


class ServiceFilterForm(BSModalForm):
    """

    Форма фильтра

    """
    NO_FILTER = 0
    choices = ((NO_FILTER, 'All'),) + InsuranceService.CATEGORIES
    category = forms.ChoiceField(choices=choices)
