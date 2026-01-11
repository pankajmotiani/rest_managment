import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from inventory.models import InventorySettings, Ingredient

print("=" * 70)
print("SETTING UP INVENTORY SYSTEM FOR KAKA CAFE")
print("=" * 70)

# Create inventory settings
settings, created = InventorySettings.objects.get_or_create(
    id=1,
    defaults={
        'is_enabled': False,  # Disabled by default
        'auto_update_on_bill': True,
        'low_stock_threshold': 10,
        'enable_alerts': True
    }
)
print(f"✓ Inventory settings created (Enabled: {settings.is_enabled})")

# Create sample ingredients for KAKA CAFE
sample_ingredients = [
    # Dairy
    ('Milk', 'l', 50, 10, 60, 80, 'Local Dairy'),
    ('Paneer', 'kg', 20, 5, 400, 600, 'Amul'),
    ('Butter', 'kg', 15, 3, 500, 700, 'Amul'),
    ('Cheese', 'kg', 12, 3, 600, 850, 'Britannia'),
    ('Curd', 'kg', 30, 8, 80, 120, 'Local Dairy'),
    
    # Vegetables
    ('Potato', 'kg', 100, 20, 30, 50, 'Vegetable Market'),
    ('Onion', 'kg', 80, 15, 40, 60, 'Vegetable Market'),
    ('Tomato', 'kg', 60, 12, 50, 80, 'Vegetable Market'),
    ('Capsicum', 'kg', 40, 8, 80, 120, 'Vegetable Market'),
    ('Cauliflower', 'kg', 30, 6, 60, 90, 'Vegetable Market'),
    
    # Spices & Masalas
    ('Salt', 'kg', 20, 5, 20, 30, 'Spice Store'),
    ('Red Chilli Powder', 'kg', 10, 2, 200, 300, 'Spice Store'),
    ('Turmeric Powder', 'kg', 8, 2, 300, 450, 'Spice Store'),
    ('Coriander Powder', 'kg', 10, 2, 250, 375, 'Spice Store'),
    ('Garam Masala', 'kg', 5, 1, 500, 750, 'Spice Store'),
    
    # Beverages
    ('Coffee Powder', 'kg', 8, 2, 800, 1200, 'Beverage Supplier'),
    ('Tea Leaves', 'kg', 12, 3, 400, 600, 'Beverage Supplier'),
    ('Sugar', 'kg', 100, 20, 50, 75, 'Beverage Supplier'),
    ('Mineral Water', 'bottle', 200, 50, 20, 40, 'Bisleri'),
    
    # Others
    ('Bread', 'pack', 50, 10, 30, 50, 'Bakery'),
    ('Wheat Flour', 'kg', 100, 20, 60, 90, 'Grocery Store'),
    ('Oil', 'l', 80, 15, 180, 250, 'Grocery Store'),
    ('Rice', 'kg', 150, 30, 80, 120, 'Grocery Store'),
    ('Lentils', 'kg', 60, 12, 120, 180, 'Grocery Store'),
]

created_count = 0
for name, unit, current, min_stock, cost, selling, supplier in sample_ingredients:
    ingredient, created = Ingredient.objects.get_or_create(
        name=name,
        defaults={
            'unit': unit,
            'current_stock': current,
            'minimum_stock': min_stock,
            'reorder_quantity': current * 1.5,
            'cost_per_unit': cost,
            'selling_price_per_unit': selling,
            'supplier': supplier,
            'is_active': True
        }
    )
    if created:
        created_count += 1
        print(f"✓ Created: {name} ({current} {unit})")

print(f"\n✓ Created {created_count} sample ingredients")

# Create sample transactions
from django.contrib.auth.models import User
from inventory.models import InventoryTransaction

admin_user = User.objects.filter(is_superuser=True).first()
if admin_user and created_count > 0:
    for ingredient in Ingredient.objects.all()[:5]:
        InventoryTransaction.objects.create(
            ingredient=ingredient,
            transaction_type='initial',
            quantity=ingredient.current_stock,
            unit_price=ingredient.cost_per_unit,
            reference="Initial Setup",
            notes="Initial stock setup",
            created_by=admin_user
        )
    print("✓ Created initial stock transactions")

print("\n" + "=" * 70)
print("INVENTORY SETUP COMPLETE!")
print("\nFeatures Available:")
print("1. Optional inventory tracking (disabled by default)")
print("2. Auto-update when bills are generated")
print("3. Low stock alerts and notifications")
print("4. Recipe management system")
print("5. Comprehensive reports")
print("\nTo enable inventory:")
print("1. Go to /inventory/")
print("2. Click 'Enable Inventory' button")
print("3. Set up recipes in Admin Panel")
print("\nAccess: http://127.0.0.1:8000/inventory/")
print("=" * 70)