from django.urls import path
from . import views

urlpatterns = [
    path('', views.customers_list, name='customers_list'),
    path('sync/', views.sync_customers, name='sync_customers'),
    path('<int:customer_id>/', views.customer_detail, name='customer_detail'),
]