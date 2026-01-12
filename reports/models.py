from django.db import models
from pos.models import Order, Bill
from decimal import Decimal

class SalesReport(models.Model):
    report_date = models.DateField()
    report_type = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ])
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_orders = models.IntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    top_selling_item = models.CharField(max_length=200, blank=True)
    top_selling_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-report_date']
    
    def __str__(self):
        return f"{self.report_type.capitalize()} Report - {self.report_date}"