from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.sales_dashboard, name='sales_dashboard'),
    path('export/<str:report_type>/', views.export_report, name='export_report'),
    path('items/', views.item_sales_report, name='item_sales_report'),
]