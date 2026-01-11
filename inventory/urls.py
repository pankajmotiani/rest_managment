from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_dashboard, name='inventory_dashboard'),
    path('toggle/', views.toggle_inventory, name='toggle_inventory'),
    path('update/<int:ingredient_id>/', views.update_stock, name='update_stock'),
]