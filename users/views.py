from django.urls import reverse_lazy
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm
)
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalCreateView
)


class CustomSignupView(BSModalCreateView):
    """

    View регистрации

    """

    form_class = CustomUserCreationForm
    template_name = 'login-signup.html'
    success_message = 'Success'
    success_url = reverse_lazy('insure_your_buddy:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Sign up'
        return context


class CustomLoginView(BSModalLoginView):
    """

    View аутентификации

    """

    form_class = CustomAuthenticationForm
    template_name = 'login-signup.html'
    success_message = 'Success'
    success_url = reverse_lazy('insure_your_buddy:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'Log in'
        return context
