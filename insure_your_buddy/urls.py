from django.urls import path
from . import views


app_name = 'insure_your_buddy'
urlpatterns = [
    path('main/', views.MainView.as_view(), name='main'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('create/', views.CreateServiceView.as_view(), name='create_service'),
    path('update/<int:pk>', views.UpdateServiceView.as_view(), name='update_service'),
    path('delete/<int:pk>', views.DeleteServiceView.as_view(), name='delete_service'),
    path('filter/', views.FilterServiceView.as_view(), name='filter'),
    path('response/<int:service_id>',
         views.CustomerResponseView.as_view(), name='response'),
    path('detail/<int:pk>', views.ServiceDetailView.as_view(), name='detail'),
    path('search_results/', views.SearchResultsView.as_view(), name='search_results')
]
