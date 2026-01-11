import os
import sys
import django

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

print("=" * 70)
print("COMPLETE KAKA CAFE RESTAURANT SYSTEM SETUP")
print("=" * 70)

# Create all apps
print("\n1. Creating all apps...")
apps = ['reports', 'customers', 'inventory']

for app in apps:
    app_dir = os.path.join(project_root, app)
    if not os.path.exists(app_dir):
        print(f"   Creating {app} app...")
        os.system(f'python manage.py startapp {app}')
        print(f"   ✓ Created {app} app")
    else:
        print(f"   ✓ {app} app already exists")

print("\n2. Creating necessary directories...")
directories = ['static', 'media', 'media/logos', 'media/qr_codes', 'templates', 
               'templates/pos', 'templates/reports', 'templates/customers', 'templates/inventory']

for directory in directories:
    dir_path = os.path.join(project_root, directory)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"   ✓ Created {directory}/")

print("\n3. Running migrations...")
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

print("\n4. Creating superuser...")
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@kakacafe.com', 'admin123')
    print("   ✓ Created superuser: admin / admin123")
else:
    print("   ✓ Superuser already exists")

print("\n5. Setting up initial data...")
from pos.models import Restaurant, Table, Category, MenuItem

# Create restaurant
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

# Create tables
if not Table.objects.exists():
    for i in range(1, 11):
        Table.objects.create(
            table_number=str(i),
            table_name=f"Table {i}",
            capacity=4 if i <= 6 else 6
        )
    print("   ✓ Created 10 tables")

print("\n" + "=" * 70)
print("SETUP COMPLETE!")
print("\n🚀 Your Restaurant Management System is ready!")
print("\n📊 Access URLs:")
print("   • Main Dashboard: http://127.0.0.1:8000")
print("   • Sales Reports: http://127.0.0.1:8000/reports/")
print("   • Customers: http://127.0.0.1:8000/customers/")
print("   • Inventory: http://127.0.0.1:8000/inventory/")
print("   • Admin Panel: http://127.0.0.1:8000/admin/")
print("\n🔑 Admin Login: admin / admin123")
print("\n📞 Restaurant: KAKA CAFE | 7022470962 | @kakacafe.blr")
print("=" * 70)