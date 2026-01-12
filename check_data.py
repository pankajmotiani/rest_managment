import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from pos.models import Order

print("=" * 60)
print("CHECKING DATA STRUCTURE")
print("=" * 60)

# Check if there are any orders
orders = Order.objects.all()
print(f"Total orders: {orders.count()}")

for order in orders[:3]:  # Check first 3 orders
    print(f"\nOrder #{order.id} - Table {order.table.table_number}")
    print(f"Status: {order.status}")
    print(f"Total: ₹{order.total}")
    
    # Check order items
    items = order.order_items.all()
    print(f"Number of items: {items.count()}")
    
    for item in items:
        print(f"  - {item.menu_item.name} x {item.quantity} = ₹{item.total}")

print("\n" + "=" * 60)
print("If items.count() shows 0 but orders exist,")
print("you need to recreate orders after fixing models.")
print("=" * 60)