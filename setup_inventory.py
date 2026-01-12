import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from inventory.models import InventorySettings, Ingredient
from pos.models import MenuItem

print("=" * 60)
print("SETTING UP INVENTORY SYSTEM")
print("=" * 60)

# Create inventory settings
settings, created = InventorySettings.objects.get_or_create(
    id=1,
    defaults={
        'is_enabled': False,  # Disabled by default
        'auto_update_on_bill': True,
        'low_stock_threshold': 10
    }
)

if created:
    print("✓ Created inventory settings (disabled by default)")
else:
    print("✓ Inventory settings already exist")

# Create sample ingredients (common for KAKA CAFE)
sample_ingredients = [
    # Dairy
    ('Milk', 'l', 50, 10, 60),
    ('Paneer', 'kg', 20, 5, 400),
    ('Butter', 'kg', 10, 2, 500),
    ('Cheese', 'kg', 15, 3, 600),
    
    # Vegetables
    ('Potato', 'kg', 100, 20, 30),
    ('Onion', 'kg', 50, 10, 40),
    ('Tomato', 'kg', 40, 8, 50),
    ('Capsicum', 'kg', 30, 5, 80),
    
    # Spices
    ('Salt', 'kg', 20, 5, 20),
    ('Red Chilli Powder', 'kg', 10, 2, 200),
    ('Turmeric Powder', 'kg', 10, 2, 300),
    ('Coriander Powder', 'kg', 10, 2, 250),
    
    # Beverages
    ('Coffee Powder', 'kg', 5, 1, 800),
    ('Tea Leaves', 'kg', 8, 2, 400),
    ('Sugar', 'kg', 50, 10, 50),
    
    # Others
    ('Bread', 'pcs', 100, 20, 30),
    ('Wheat Flour', 'kg', 100, 20, 60),
    ('Oil', 'l', 50, 10, 180),
    ('Water Bottle', 'pcs', 200, 50, 20),
]

for name, unit, current_stock, min_stock, cost in sample_ingredients:
    ingredient, created = Ingredient.objects.get_or_create(
        name=name,
        defaults={
            'unit': unit,
            'current_stock': current_stock,
            'minimum_stock': min_stock,
            'cost_per_unit': cost,
            'supplier': 'Local Supplier'
        }
    )
    if created:
        print(f"✓ Created ingredient: {name}")

print("\n" + "=" * 60)
print("INVENTORY SETUP COMPLETE!")
print("\nFeatures:")
print("1. Optional inventory tracking (disabled by default)")
print("2. Auto-update when bills are generated")
print("3. Low stock alerts")
print("4. Recipe management")
print("\nTo enable inventory:")
print("1. Go to /inventory/")
print("2. Click 'Enable Inventory' button")
print("3. Set up recipes in Admin Panel")
print("=" * 60)