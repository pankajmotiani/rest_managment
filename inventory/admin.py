from django.contrib import admin
from .models import *

@admin.register(InventorySettings)
class InventorySettingsAdmin(admin.ModelAdmin):
    list_display = ['is_enabled', 'auto_update_on_bill', 'low_stock_threshold']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'current_stock', 'minimum_stock', 'is_low_stock', 'is_active']
    list_filter = ['is_active', 'unit']
    search_fields = ['name']
    actions = ['mark_active', 'mark_inactive']
    
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = "Mark selected ingredients as active"
    
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected ingredients as inactive"

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['menu_item']
    filter_horizontal = ['ingredients']
    search_fields = ['menu_item__name']

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'quantity_required']
    list_filter = ['recipe__menu_item']

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'transaction_type', 'quantity', 'previous_stock', 'new_stock', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['ingredient__name', 'reference']
    readonly_fields = ['created_at']