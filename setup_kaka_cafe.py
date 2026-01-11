import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from django.contrib.auth.models import User
from pos.models import Restaurant, Table

print("=" * 60)
print("SETTING UP KAKA CAFE BILLING SYSTEM")
print("=" * 60)

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@kakacafe.com', 'admin123')
    print("✓ Superuser created: admin / admin123")
else:
    print("✓ Superuser already exists")

# Create restaurant details
restaurant, created = Restaurant.objects.update_or_create(
    id=1,
    defaults={
        'name': 'KAKA CAFE',
        'address': 'Bangalore',
        'phone': '7022470962',
        'email': 'contact@kakacafe.com',
        'gstin': '',
    }
)
print(f"✓ Restaurant details: {restaurant.name}")
print(f"  Contact: {restaurant.phone}")
print(f"  Instagram: @kakacafe.blr")

# Create tables
if not Table.objects.exists():
    tables = [
        ("1", "Window Table", 4),
        ("2", "Center Table", 4),
        ("3", "Family Table", 6),
        ("4", "Corner Table", 2),
        ("5", "VIP Table", 8),
        ("6", "Regular", 4),
        ("7", "Regular", 4),
        ("8", "Regular", 4),
        ("9", "Regular", 4),
        ("10", "Regular", 4),
    ]
    
    for number, name, capacity in tables:
        Table.objects.create(
            table_number=number,
            table_name=name,
            capacity=capacity
        )
    print(f"✓ Created {len(tables)} tables")

print("\n" + "=" * 60)
print("SETUP COMPLETE!")
print("\nNext steps:")
print("1. Run menu import: python manual_import.py")
print("2. Start server: python manage.py runserver")
print("\nAccess links:")
print("- Billing System: http://127.0.0.1:8000")
print("- Admin Panel: http://127.0.0.1:8000/admin")
print("\nAdmin login: admin / admin123")
print("=" * 60)