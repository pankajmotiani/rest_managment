import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from pos.models import MenuItem, Category, Order, OrderItem, Bill
from django.contrib.auth.models import User

print("=" * 60)
print("RESETTING KAKA CAFE SYSTEM")
print("=" * 60)

# Delete all old data
MenuItem.objects.all().delete()
print("✓ Cleared old menu items")

Category.objects.all().delete()
print("✓ Cleared old categories")

OrderItem.objects.all().delete()
print("✓ Cleared order items")

Order.objects.all().delete()
print("✓ Cleared orders")

Bill.objects.all().delete()
print("✓ Cleared bills")

# Reset all tables to available
from pos.models import Table
Table.objects.update(status='available')
print("✓ Reset all tables to available")

print("\nSystem reset complete!")
print("Now run: python fresh_import.py")
print("=" * 60)