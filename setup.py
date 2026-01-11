import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from django.contrib.auth.models import User
from pos.models import Restaurant, Category, MenuItem, Table

print("Setting up Restaurant Billing System...")
print("=" * 60)

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@restaurant.com', 'admin123')
    print("✓ Superuser created: admin / admin123")

# Create restaurant
if not Restaurant.objects.exists():
    Restaurant.objects.create(
        name="Delicious Bites Restaurant",
        address="123 Food Street, Mumbai - 400001",
        phone="+91 9876543210",
        email="info@deliciousbites.com",
        gstin="27AABCS1429B1Z"
    )
    print("✓ Restaurant details created")

# Create tables
if not Table.objects.exists():
    tables = [
        ("1", "Window View", 4),
        ("2", "Family Table", 6),
        ("3", "Couple Table", 2),
        ("4", "Center Table", 4),
        ("5", "VIP Table", 8),
        ("6", "Regular", 4),
        ("7", "Regular", 4),
        ("8", "Regular", 4),
    ]
    
    for number, name, capacity in tables:
        Table.objects.create(
            table_number=number,
            table_name=name,
            capacity=capacity
        )
    print(f"✓ Created {len(tables)} tables")

# Create categories and menu
if not Category.objects.exists():
    menu_data = {
        "Starters": [
            ("Garlic Bread", "Freshly baked with garlic butter", 120),
            ("Spring Rolls", "Crispy vegetable rolls", 150),
            ("Chicken Wings", "Spicy buffalo wings", 180),
            ("Paneer Tikka", "Grilled cottage cheese", 160),
        ],
        "Main Course": [
            ("Butter Chicken", "Chicken in rich tomato gravy", 320),
            ("Paneer Butter Masala", "Cottage cheese in creamy sauce", 280),
            ("Veg Biryani", "Fragrant rice with vegetables", 220),
            ("Chicken Biryani", "Hyderabadi style biryani", 280),
        ],
        "Chinese": [
            ("Veg Hakka Noodles", "Stir-fried noodles", 180),
            ("Chicken Manchurian", "Spicy chicken balls", 220),
            ("Veg Fried Rice", "Classic fried rice", 160),
            ("Chilli Chicken", "Spicy chilli chicken", 240),
        ],
        "Beverages": [
            ("Fresh Lime Soda", "Refreshing soda", 60),
            ("Cold Coffee", "Iced coffee with cream", 90),
            ("Masala Chai", "Spiced Indian tea", 40),
            ("Mineral Water", "1 liter bottle", 20),
        ],
        "Desserts": [
            ("Chocolate Brownie", "With vanilla ice cream", 150),
            ("Gulab Jamun", "Sweet milk balls", 120),
            ("Ice Cream", "Vanilla/Chocolate/Strawberry", 100),
            ("Chocolate Mousse", "Rich chocolate dessert", 140),
        ]
    }
    
    for order, (category_name, items) in enumerate(menu_data.items(), 1):
        category = Category.objects.create(
            name=category_name,
            display_order=order
        )
        
        for item_name, description, price in items:
            MenuItem.objects.create(
                category=category,
                name=item_name,
                description=description,
                price=price
            )
    
    print(f"✓ Created menu with {len(menu_data)} categories")

print("=" * 60)
print("SETUP COMPLETE!")
print("\nTo start the system:")
print("1. python manage.py runserver")
print("\nAccess links:")
print("- Admin Panel: http://127.0.0.1:8000/admin")
print("- Billing System: http://127.0.0.1:8000")
print("\nLogin: admin / admin123")