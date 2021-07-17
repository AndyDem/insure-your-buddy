from bootstrap_modal_forms.forms import BSModalModelForm
from .models import InsuranceService, Customer


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