from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('main', views.MainView, name='main'),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("signup/", views.CustomSignupView.as_view(), name="signup"),
    path('create', views.CreateServiceView.as_view(), name='create'),
    path('update/<int:pk>', views.UpdateServiceView.as_view(), name='update'),
    path('delete/<int:pk>', views.DeleteServiceView.as_view(), name='delete'),
    path('filter/', views.ServiceFilterView.as_view(), name='filter')
]
