import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

print("=" * 60)
print("SETTING UP NEW FEATURES")
print("=" * 60)

# Create new apps
print("\n1. Creating new apps...")
os.system('python manage.py startapp reports')
os.system('python manage.py startapp customers')
os.system('python manage.py startapp inventory')

print("\n2. Updating settings.py...")
# Add to INSTALLED_APPS: 'reports', 'customers', 'inventory'

print("\n3. Creating migrations...")
os.system('python manage.py makemigrations')

print("\n4. Applying migrations...")
os.system('python manage.py migrate')

print("\n" + "=" * 60)
print("SETUP COMPLETE!")
print("\nNew Features Added:")
print("1. Auto-scroll category tabs in menu")
print("2. Sales reports (daily, weekly, monthly)")
print("3. Customer database with phone numbers")
print("4. Inventory management (optional)")
print("\nAccess URLs:")
print("- Reports: http://127.0.0.1:8000/reports/")
print("- Customers: http://127.0.0.1:8000/customers/")
print("- Inventory: http://127.0.0.1:8000/inventory/")
print("=" * 60)