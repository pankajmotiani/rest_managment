from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'total_orders', 'total_spent', 'last_order_date']
    search_fields = ['name', 'phone']
    list_filter = ['last_order_date']