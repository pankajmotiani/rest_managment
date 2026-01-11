import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from django.contrib.auth.models import User
from pos.models import *
import shutil

print("=" * 60)
print("COMPLETE RESET - KAKA CAFE BILLING SYSTEM")
print("=" * 60)

# Delete all data
print("\nClearing all data...")
MenuItem.objects.all().delete()
print("✓ Cleared menu items")

Category.objects.all().delete()
print("✓ Cleared categories")

OrderItem.objects.all().delete()
print("✓ Cleared order items")

Order.objects.all().delete()
print("✓ Cleared orders")

Bill.objects.all().delete()
print("✓ Cleared bills")

Table.objects.all().delete()
print("✓ Cleared tables")

Restaurant.objects.all().delete()
print("✓ Cleared restaurant info")

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@kakacafe.com', 'admin123')
    print("\n✓ Created superuser: admin / admin123")
else:
    print("\n✓ Superuser already exists")

# Create restaurant
Restaurant.objects.create(
    name='KAKA CAFE',
    address='Bangalore',
    phone='7022470962',
    email='contact@kakacafe.com'
)
print("✓ Created restaurant: KAKA CAFE")

# Create tables
tables = [
    ("1", "Table 1", 4),
    ("2", "Table 2", 4),
    ("3", "Table 3", 4),
    ("4", "Table 4", 4),
    ("5", "Table 5", 6),
    ("6", "Table 6", 6),
    ("7", "Table 7", 2),
    ("8", "Table 8", 2),
    ("9", "Table 9", 8),
    ("10", "Table 10", 8),
]

for number, name, capacity in tables:
    Table.objects.create(
        table_number=number,
        table_name=name,
        capacity=capacity
    )
print(f"✓ Created {len(tables)} tables")

print("\n" + "=" * 60)
print("BASIC SETUP COMPLETE!")
print("\nNow run: python import_kaka_menu.py")
print("Then: python manage.py runserver")
print("=" * 60)