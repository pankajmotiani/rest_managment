import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from pos.models import Restaurant, Category, MenuItem

def import_kaka_cafe_menu():
    print("=" * 60)
    print("IMPORTING KAKA CAFE MENU")
    print("=" * 60)
    
    # Update restaurant details
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
    print(f"✓ Restaurant updated: {restaurant.name}")
    print(f"  Contact: {restaurant.phone}")
    print(f"  Instagram: @kakacafe.blr")
    print(f"  Timing: 9:30 AM - 11:30 PM")
    
    # Define menu data from PDF
    menu_data = {
        'Quick Bites': [
            ('French Fries', 90),
            ('Peri Peri French Fries', 110),
            ('Chilli Garlic Bites', 130),
            ('Cheese Grilled Sandwich', 140),
            ('Maggie', 40),
            ('Veg Maggie', 60),
            ('Bread Butter', 35),
            ('Green Salad', 45),
        ],
        'Desi Starters': [
            ('Bhel Puri', 45),
            ('Dal Pakwaan', 140),
            ('Dahi Pakwaan', 120),
            ('Desi Crispy Corn', 90),
            ('Masala Corn', 70),
            ('Crispy Corn', 120),
            ('Masala Papad', 50),
            ('Cheese Masala Papad', 75),
        ],
        'Chinese Starters': [
            ('Chilly Paneer', 200),
            ('Paneer Manchurian', 210),
            ('Paneer 65', 210),
            ('Gobi Manchurian', 190),
            ('Chilly Gobi', 180),
        ],
        'Parathas': [
            ('Aloo Paratha', 100),
            ('Onion Paratha', 100),
            ('Gobi Paratha', 110),
            ('Paneer Paratha', 130),
            ('Garlic Paratha', 130),
            ('Cheese Paratha', 140),
            ('Kaka Special Paratha', 140),
            ('Kaka Cheese Special Paratha', 160),
        ],
        'Paneer Special': [
            ('Paneer Butter Masala', 210),
            ('Kadai Paneer', 230),
            ('Paneer Bhurji', 240),
            ('Matar Paneer', 230),
            ('Kaju Paneer', 250),
        ],
        'Curries': [
            ('Kaju Curry', 240),
            ('Mushroom Masala', 240),
            ('Jeera Aloo (Dry)', 120),
            ('Aloo Tamatar', 120),
            ('Aloo Matar', 140),
            ('Aloo Gobi', 130),
            ('Mix Veg', 180),
            ('Veg Kolhapuri', 190),
        ],
        'Dals': [
            ('Dal Makhani', 180),
            ('Dal Tadka', 160),
            ('Dal Fry', 150),
        ],
        'Rajasthani Special': [
            ('Sev Tamatar', 170),
            ('Dudh Sev Tamatar', 180),
            ('Besan Kadhi', 150),
            ('Jaipuriya Papad', 190),
            ('Dal Bati Churma Thali', 250),
        ],
        'Breads': [
            ('Roti', 20),
            ('Ghee Roti', 25),
        ],
        'Rice': [
            ('Jeera Rice', 150),
            ('Curd Rice', 170),
            ('Ghee Rice', 190),
            ('Veg Fried Rice', 180),
            ('Paneer Fried Rice', 210),
        ],
        'Hot Beverages': [
            ('Tea', 15),
            ('Lemon Tea', 20),
            ('Coffee', 20),
        ],
        'Cold Beverages': [
            ('Cold Coffee', 80),
            ('Cold Coffee with Icecream', 100),
            ('Iced Tea', 80),
            ('Butter Milk', 30),
            ('Lassi', 80),
            ('Dry Fruit Lassi', 90),
            ('Lemonade', 50),
            ('Mint Mojito', 120),
            ('Blue Lagoon', 140),
        ],
        'Desserts': [
            ('Churma', 50),
            ('Shahi Crunch (with Icecream)', 180),
            ('Sindhi Gurari (Jaggery Stuffing)', 190),
            ('Sindhi Shahi Gurari (Jaggery Stuffing with Dryfruits)', 199),
        ],
    }
    
    # Define category order
    category_order = {
        'Quick Bites': 1,
        'Desi Starters': 2,
        'Chinese Starters': 3,
        'Parathas': 4,
        'Paneer Special': 5,
        'Curries': 6,
        'Dals': 7,
        'Rajasthani Special': 8,
        'Breads': 9,
        'Rice': 10,
        'Hot Beverages': 11,
        'Cold Beverages': 12,
        'Desserts': 13,
    }
    
    total_items = 0
    
    # Create categories and import items
    for category_name, items in menu_data.items():
        # Create category
        category, cat_created = Category.objects.get_or_create(
            name=category_name,
            defaults={'display_order': category_order.get(category_name, 99)}
        )
        
        if cat_created:
            print(f"\n✓ Created category: {category_name}")
        
        # Add items
        category_count = 0
        for item_name, price in items:
            menu_item, item_created = MenuItem.objects.update_or_create(
                name=item_name,
                category=category,
                defaults={
                    'price': price,
                    'description': f'KAKA CAFE Special - {item_name}',
                    'is_available': True
                }
            )
            
            if item_created:
                category_count += 1
                total_items += 1
        
        if category_count > 0:
            print(f"  Added {category_count} items to {category_name}")
    
    print("\n" + "=" * 60)
    print("IMPORT COMPLETE!")
    print(f"Total menu items imported: {total_items}")
    print("\nMenu Categories:")
    
    for category in Category.objects.all().order_by('display_order'):
        item_count = MenuItem.objects.filter(category=category).count()
        if item_count > 0:
            print(f"  • {category.name}: {item_count} items")
    
    print("\nAccess your billing system at: http://127.0.0.1:8000")
    print("=" * 60)

if __name__ == '__main__':
    import_kaka_cafe_menu()