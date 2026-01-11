import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from django.contrib.auth.models import User
from pos.models import *

print("=" * 60)
print("FIXING BILL PRINTING - TEST SCRIPT")
print("=" * 60)

# Create test data
print("\n1. Creating test restaurant...")
restaurant, created = Restaurant.objects.update_or_create(
    id=1,
    defaults={
        'name': 'KAKA CAFE',
        'address': 'Bangalore',
        'phone': '7022470962',
        'email': 'contact@kakacafe.com',
    }
)
print(f"   ✓ Restaurant: {restaurant.name}")

print("\n2. Creating test table...")
table, created = Table.objects.get_or_create(
    table_number='99',
    defaults={
        'table_name': 'Test Table',
        'capacity': 4,
        'status': 'available'
    }
)
print(f"   ✓ Table: {table.table_number}")

print("\n3. Creating test category and menu items...")
category, created = Category.objects.get_or_create(
    name='Test Category',
    defaults={'display_order': 99}
)

# Create test menu items
test_items = [
    ('Test Burger', 150),
    ('Test Fries', 80),
    ('Test Coke', 60),
]

for item_name, price in test_items:
    item, created = MenuItem.objects.get_or_create(
        name=item_name,
        category=category,
        defaults={
            'price': price,
            'is_available': True
        }
    )
    print(f"   ✓ Menu Item: {item_name} - ₹{price}")

print("\n4. Creating test order...")
# Clear any existing test order
Order.objects.filter(table=table).delete()

order = Order.objects.create(
    table=table,
    customer_name='Test Customer',
    status='active'
)
print(f"   ✓ Order #{order.id} created")

print("\n5. Adding items to order...")
menu_items = MenuItem.objects.filter(category=category)[:3]

for i, menu_item in enumerate(menu_items):
    OrderItem.objects.create(
        order=order,
        menu_item=menu_item,
        quantity=i + 1,
        price=menu_item.price
    )
    print(f"   ✓ Added: {menu_item.name} x {i+1}")

print("\n6. Calculating totals...")
order.calculate_totals()
print(f"   ✓ Subtotal: ₹{order.subtotal}")
print(f"   ✓ Total: ₹{order.total}")

print("\n7. Creating test bill...")
bill = Bill.objects.create(
    order=order,
    payment_method='cash',
    paid_amount=order.total
)
print(f"   ✓ Bill #{bill.bill_number} created")

print("\n" + "=" * 60)
print("TEST DATA CREATED SUCCESSFULLY!")
print("\nTest URLs:")
print(f"1. View Order: http://127.0.0.1:8000/table/{table.id}/")
print(f"2. Generate Bill: http://127.0.0.1:8000/bill/{order.id}/")
print(f"3. Print Bill: http://127.0.0.1:8000/print-bill/{bill.id}/")
print("\nExpected Results:")
print("- All 3 items should show in bill")
print("- Quantities should show correctly")
print("- Prices and totals should calculate properly")
print("=" * 60)