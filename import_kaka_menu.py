import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from pos.models import Category, MenuItem

print("=" * 60)
print("IMPORTING KAKA CAFE MENU")
print("=" * 60)

# Define categories
categories = [
    ('Quick Bites', 1),
    ('Desi Starters', 2),
    ('Chinese Starters', 3),
    ('Parathas', 4),
    ('Paneer Special', 5),
    ('Curries', 6),
    ('Dals', 7),
    ('Rajasthani Special', 8),
    ('Breads', 9),
    ('Rice', 10),
    ('Hot Beverages', 11),
    ('Cold Beverages', 12),
    ('Desserts', 13),
]

# Create categories
category_objects = {}
for cat_name, order in categories:
    category, created = Category.objects.get_or_create(
        name=cat_name,
        defaults={'display_order': order}
    )
    category_objects[cat_name] = category
    print(f"✓ Category: {cat_name}")

# Complete KAKA CAFE menu from PDF
menu_data = [
    # Quick Bites
    ('Quick Bites', 'French Fries', 90),
    ('Quick Bites', 'Peri Peri French Fries', 110),
    ('Quick Bites', 'Chilli Garlic Bites', 130),
    ('Quick Bites', 'Cheese Grilled Sandwich', 140),
    ('Quick Bites', 'Maggie', 40),
    ('Quick Bites', 'Veg Maggie', 60),
    ('Quick Bites', 'Bread Butter', 35),
    ('Quick Bites', 'Green Salad', 45),
    
    # Desi Starters
    ('Desi Starters', 'Bhel Puri', 45),
    ('Desi Starters', 'Dal Pakwaan', 140),
    ('Desi Starters', 'Dahi Pakwaan', 120),
    ('Desi Starters', 'Desi Crispy Corn', 90),
    ('Desi Starters', 'Masala Corn', 70),
    ('Desi Starters', 'Crispy Corn', 120),
    ('Desi Starters', 'Masala Papad', 50),
    ('Desi Starters', 'Cheese Masala Papad', 75),
    
    # Chinese Starters
    ('Chinese Starters', 'Chilly Paneer', 200),
    ('Chinese Starters', 'Paneer Manchurian', 210),
    ('Chinese Starters', 'Paneer 65', 210),
    ('Chinese Starters', 'Gobi Manchurian', 190),
    ('Chinese Starters', 'Chilly Gobi', 180),
    
    # Parathas
    ('Parathas', 'Aloo Paratha', 100),
    ('Parathas', 'Onion Paratha', 100),
    ('Parathas', 'Gobi Paratha', 110),
    ('Parathas', 'Paneer Paratha', 130),
    ('Parathas', 'Garlic Paratha', 130),
    ('Parathas', 'Cheese Paratha', 140),
    ('Parathas', 'Kaka Special Paratha', 140),
    ('Parathas', 'Kaka Cheese Special Paratha', 160),
    
    # Paneer Special
    ('Paneer Special', 'Paneer Butter Masala', 210),
    ('Paneer Special', 'Kadai Paneer', 230),
    ('Paneer Special', 'Paneer Bhurji', 240),
    ('Paneer Special', 'Matar Paneer', 230),
    ('Paneer Special', 'Kaju Paneer', 250),
    
    # Curries
    ('Curries', 'Kaju Curry', 240),
    ('Curries', 'Mushroom Masala', 240),
    ('Curries', 'Jeera Aloo (Dry)', 120),
    ('Curries', 'Aloo Tamatar', 120),
    ('Curries', 'Aloo Matar', 140),
    ('Curries', 'Aloo Gobi', 130),
    ('Curries', 'Mix Veg', 180),
    ('Curries', 'Veg Kolhapuri', 190),
    
    # Dals
    ('Dals', 'Dal Makhani', 180),
    ('Dals', 'Dal Tadka', 160),
    ('Dals', 'Dal Fry', 150),
    
    # Rajasthani Special
    ('Rajasthani Special', 'Sev Tamatar', 170),
    ('Rajasthani Special', 'Dudh Sev Tamatar', 180),
    ('Rajasthani Special', 'Besan Kadhi', 150),
    ('Rajasthani Special', 'Jaipuriya Papad', 190),
    ('Rajasthani Special', 'Dal Bati Churma Thali', 250),
    
    # Breads
    ('Breads', 'Roti', 20),
    ('Breads', 'Ghee Roti', 25),
    
    # Rice
    ('Rice', 'Jeera Rice', 150),
    ('Rice', 'Curd Rice', 170),
    ('Rice', 'Ghee Rice', 190),
    ('Rice', 'Veg Fried Rice', 180),
    ('Rice', 'Paneer Fried Rice', 210),
    
    # Hot Beverages
    ('Hot Beverages', 'Tea', 15),
    ('Hot Beverages', 'Lemon Tea', 20),
    ('Hot Beverages', 'Coffee', 20),
    
    # Cold Beverages
    ('Cold Beverages', 'Cold Coffee', 80),
    ('Cold Beverages', 'Cold Coffee with Icecream', 100),
    ('Cold Beverages', 'Iced Tea', 80),
    ('Cold Beverages', 'Butter Milk', 30),
    ('Cold Beverages', 'Lassi', 80),
    ('Cold Beverages', 'Dry Fruit Lassi', 90),
    ('Cold Beverages', 'Lemonade', 50),
    ('Cold Beverages', 'Mint Mojito', 120),
    ('Cold Beverages', 'Blue Lagoon', 140),
    
    # Desserts
    ('Desserts', 'Churma', 50),
    ('Desserts', 'Shahi Crunch (with Icecream)', 180),
    ('Desserts', 'Sindhi Gurari (Jaggery Stuffing)', 190),
    ('Desserts', 'Sindhi Shahi Gurari (Jaggery Stuffing with Dryfruits)', 199),
]

# Import menu items
imported = 0
for category_name, item_name, price in menu_data:
    category = category_objects[category_name]
    
    MenuItem.objects.create(
        category=category,
        name=item_name,
        price=price,
        is_available=True
    )
    imported += 1

print(f"\n✓ Imported {imported} menu items")

# Display summary
print("\n" + "=" * 60)
print("MENU SUMMARY")
print("=" * 60)

for cat_name, category in category_objects.items():
    count = MenuItem.objects.filter(category=category).count()
    print(f"{cat_name}: {count} items")

print("=" * 60)
print("\n✅ SYSTEM READY!")
print("\nRun: python manage.py runserver")
print("Access: http://127.0.0.1:8000")
print("Admin: http://127.0.0.1:8000/admin (admin/admin123)")
print("=" * 60)