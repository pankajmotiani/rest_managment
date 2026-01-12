from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('table/<int:table_id>/', views.table_detail, name='table_detail'),
    path('add-item/', views.add_item, name='add_item'),
    path('update-item/', views.update_item_quantity, name='update_item'),
    path('update-charges/', views.update_charges, name='update_charges'),
    path('bill/<int:order_id>/', views.generate_bill, name='generate_bill'),
    path('print-bill/<int:bill_id>/', views.print_bill, name='print_bill'),
]