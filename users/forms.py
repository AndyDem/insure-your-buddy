from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    """
    
    Форма для регистрации пользователя (компании)
    
    """
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'company_name',
            'email'
        ]


class CustomAuthenticationForm(PopRequestMixin, CreateUpdateAjaxMixin, AuthenticationForm):
    """
    
    Форма для аутентификации пользователя (компании)
    
    """
    pass
