from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class InventorySettings(models.Model):
    is_enabled = models.BooleanField(default=False)
    low_stock_threshold = models.IntegerField(default=10)
    
    def __str__(self):
        return "Inventory Settings"

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('pcs', 'Pieces'),
        ('pack', 'Packets'),
    ]
    
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pcs')
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    supplier = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"
    
    @property
    def status(self):
        if self.current_stock <= 0:
            return 'out_of_stock'
        elif self.current_stock <= self.minimum_stock:
            return 'low_stock'
        else:
            return 'in_stock'

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', 'Purchase'),
        ('consumption', 'Consumption'),
        ('adjustment', 'Adjustment'),
    ]
    
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_type} - {self.ingredient.name}: {self.quantity}"
    
    def save(self, *args, **kwargs):
        # Update ingredient stock
        ingredient = self.ingredient
        
        if self.transaction_type == 'purchase':
            ingredient.current_stock += self.quantity
        elif self.transaction_type == 'consumption':
            ingredient.current_stock -= self.quantity
        elif self.transaction_type == 'adjustment':
            ingredient.current_stock = self.quantity
        
        ingredient.save()
        super().save(*args, **kwargs)