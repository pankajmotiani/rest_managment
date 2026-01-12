from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_dashboard, name='inventory_dashboard'),
    path('toggle/', views.toggle_inventory, name='toggle_inventory'),
    path('ingredient/<int:ingredient_id>/', views.ingredient_detail, name='ingredient_detail'),
    path('ingredient/<int:ingredient_id>/update/', views.update_stock, name='update_stock'),
    path('recipes/', views.recipe_management, name='recipe_management'),
    path('recipes/create/', views.create_recipe, name='create_recipe'),
    path('reports/', views.inventory_reports, name='inventory_reports'),
]