from django.db import models
from pos.models import MenuItem
from decimal import Decimal

class InventorySettings(models.Model):
    """Settings to enable/disable inventory tracking"""
    is_enabled = models.BooleanField(default=False, help_text="Enable inventory tracking")
    auto_update_on_bill = models.BooleanField(default=True, help_text="Auto update inventory when bill is generated")
    low_stock_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=10, help_text="Low stock alert threshold")
    
    def __str__(self):
        return "Inventory Settings"
    
    class Meta:
        verbose_name_plural = "Inventory Settings"

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('pcs', 'Pieces'),
        ('pack', 'Packets'),
    ]
    
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    supplier = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock

class Recipe(models.Model):
    """Link menu items to ingredients"""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    
    def __str__(self):
        return f"Recipe for {self.menu_item.name}"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity required per serving")
    
    def __str__(self):
        return f"{self.recipe.menu_item.name} - {self.ingredient.name}: {self.quantity_required}"

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', 'Purchase'),
        ('consumption', 'Consumption'),
        ('adjustment', 'Adjustment'),
        ('waste', 'Waste'),
    ]
    
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    previous_stock = models.DecimalField(max_digits=10, decimal_places=2)
    new_stock = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Update ingredient stock
        if self.transaction_type == 'purchase':
            self.ingredient.current_stock += self.quantity
        elif self.transaction_type in ['consumption', 'waste']:
            self.ingredient.current_stock -= self.quantity
        elif self.transaction_type == 'adjustment':
            self.ingredient.current_stock = self.new_stock
        
        self.previous_stock = self.ingredient.current_stock - self.quantity
        self.new_stock = self.ingredient.current_stock
        
        super().save(*args, **kwargs)
        self.ingredient.save()
    
    def __str__(self):
        return f"{self.transaction_type} - {self.ingredient.name}: {self.quantity}"