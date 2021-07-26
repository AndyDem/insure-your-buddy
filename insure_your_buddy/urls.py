from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('main', views.main_view, name='main'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.CustomSignupView.as_view(), name='signup'),
    path('create/', views.CreateServiceView.as_view(), name='create_service'),
    # path('update/<int:pk>', views.UpdateServiceView.as_view(), name='update_service'),
    path('delete/<int:pk>', views.DeleteServiceView.as_view(), name='delete_service'),
    path('filter/', views.FilterServiceView.as_view(), name='filter'),
    path('response/<int:service_id>',views.CustomerResponseView.as_view(), name='response'),
    path('show/<int:service_id>',views.show_responses_view, name='show_responses')
]
