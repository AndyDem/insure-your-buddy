from django import forms
from bootstrap_modal_forms.forms import BSModalForm, BSModalModelForm
from .models import InsuranceService, Customer
from django.contrib.auth import get_user_model


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
    NO_FILTER = ((0, 'All'),)

    CATEGORIES = NO_FILTER + InsuranceService.CATEGORIES
    MINIMAL_PAYMENTS = NO_FILTER + (
        ('0 100', '< 100$'),
        ('100 1000', '100$ - 1000$'),
        ('1000 1000000000', '> 1000$')
    )
    TERMS = NO_FILTER + (
        ('0 6', '< 6 months'),
        ('6 12', '6 to 12 months'),
        ('12 1000', '> 12 months')
    )

    def __init__(self, *args, **kwargs):
        super(ServiceFilterForm, self).__init__(*args, **kwargs)
        self.fields['company'].choices = self.NO_FILTER + tuple(
            (user.id, user.company_name) for user in
            get_user_model().objects.filter(is_superuser=False)
        )

    category = forms.ChoiceField(choices=CATEGORIES)
    minimal_payment = forms.ChoiceField(choices=MINIMAL_PAYMENTS)
    term = forms.ChoiceField(choices=TERMS)
    company = forms.ChoiceField()


class SearchForm(BSModalForm):
    search = forms.CharField()
