from django.urls import path
from . import views

urlpatterns = [
    path('main', views.MainView, name='main'),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("signup/", views.CustomSignupView.as_view(), name="signup"),
    path('create', views.CreateServiceView.as_view(), name='create'),
    path('update/<int:pk>', views.UpdateServiceView.as_view(), name='update'),
    path('delete/<int:pk>', views.DeleteServiceView.as_view(), name='delete'),
]
