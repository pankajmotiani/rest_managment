from django.contrib import admin
from .models import InventorySettings, Ingredient, InventoryTransaction

@admin.register(InventorySettings)
class InventorySettingsAdmin(admin.ModelAdmin):
    list_display = ['is_enabled', 'low_stock_threshold']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'current_stock', 'minimum_stock', 'status', 'is_active']
    list_filter = ['unit', 'is_active']
    search_fields = ['name', 'supplier']

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'transaction_type', 'quantity', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['ingredient__name', 'reference']