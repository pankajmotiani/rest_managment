import os
import django
import PyPDF2
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from pos.models import Restaurant, Category, MenuItem, Table

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
    
    return text

def parse_menu(text):
    """Parse the extracted text to get menu items"""
    
    # Extract restaurant name and contact
    restaurant_name = "KAKA CAFE"
    phone = "7022470962"
    
    # Clean up the text
    lines = text.split('\n')
    
    # Define categories based on your PDF
    categories_mapping = {
        'QUICK BITES': 'Quick Bites',
        'DESI STARTERS': 'Desi Starters',
        'CHIENSE STARTERS': 'Chinese Starters',  # Fixed typo
        'PARATHAS': 'Parathas',
        'CURRIES': 'Curries',
        'PANER SPECIAL': 'Paneer Special',
        'DALS': 'Dals',
        'RAJASTHANI SPECIAL': 'Rajasthani Special',
        'BREADS': 'Breads',
        'RICE': 'Rice',
        'BEVERAGE': 'Beverages',
        'HOT': 'Hot Beverages',
        'COLD': 'Cold Beverages',
        'DESSERT': 'Desserts',
    }
    
    # Alternative parsing approach
    menu_data = []
    
    # Extract items with prices using regex
    price_pattern = r'(\d+)\s*$'
    
    current_category = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line contains a category name
        for pdf_cat, db_cat in categories_mapping.items():
            if pdf_cat in line.upper():
                current_category = db_cat
                print(f"Found category: {current_category}")
                break
        
        # Check if line contains price (ends with digits)
        if re.search(price_pattern, line) and current_category:
            # Remove price from end
            item_name = re.sub(price_pattern, '', line).strip()
            price_match = re.search(price_pattern, line)
            if price_match:
                price = int(price_match.group(1))
                
                # Clean up item name
                item_name = item_name.replace('|', '').replace('-', '').strip()
                
                if item_name and price > 0:
                    menu_data.append({
                        'category': current_category,
                        'name': item_name,
                        'price': price
                    })
                    print(f"  - {item_name}: ₹{price}")
    
    return restaurant_name, phone, menu_data

def import_menu_from_pdf(pdf_path):
    print("=" * 60)
    print("IMPORTING KAKA CAFE MENU FROM PDF")
    print("=" * 60)
    
    # Extract text from PDF
    print("\nExtracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    # Parse menu
    print("\nParsing menu items...")
    restaurant_name, phone, menu_items = parse_menu(text)
    
    # Update restaurant details
    print(f"\nUpdating restaurant details: {restaurant_name}")
    restaurant, created = Restaurant.objects.update_or_create(
        id=1,
        defaults={
            'name': restaurant_name,
            'address': 'Bangalore (Check PDF for address)',
            'phone': phone,
            'email': 'contact@kakacafe.com',
            'gstin': '',  # Add if available
        }
    )
    
    # Create categories
    print("\nCreating categories...")
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
        'Beverages': 11,
        'Hot Beverages': 12,
        'Cold Beverages': 13,
        'Desserts': 14,
    }
    
    # First, create all categories
    for cat_name, order in category_order.items():
        Category.objects.get_or_create(
            name=cat_name,
            defaults={'display_order': order}
        )
        print(f"✓ Created category: {cat_name}")
    
    # Import menu items
    print("\nImporting menu items...")
    imported_count = 0
    
    for item in menu_items:
        try:
            category = Category.objects.get(name=item['category'])
            
            # Check if item already exists
            existing_item = MenuItem.objects.filter(
                name__iexact=item['name'],
                category=category
            ).first()
            
            if not existing_item:
                MenuItem.objects.create(
                    category=category,
                    name=item['name'],
                    price=item['price'],
                    description=f"KAKA CAFE Special - {item['name']}",
                    is_available=True
                )
                imported_count += 1
                print(f"✓ Added: {item['name']} - ₹{item['price']}")
            else:
                # Update price if different
                if existing_item.price != item['price']:
                    existing_item.price = item['price']
                    existing_item.save()
                    print(f"↻ Updated price: {item['name']} - ₹{item['price']}")
                
        except Category.DoesNotExist:
            print(f"✗ Category not found: {item['category']}")
        except Exception as e:
            print(f"✗ Error importing {item['name']}: {e}")
    
    print("\n" + "=" * 60)
    print(f"IMPORT COMPLETE!")
    print(f"Restaurant: {restaurant_name}")
    print(f"Contact: {phone}")
    print(f"Menu items imported/updated: {imported_count}")
    print("=" * 60)
    
    # Display summary
    print("\nMENU SUMMARY:")
    for category in Category.objects.all().order_by('display_order'):
        count = MenuItem.objects.filter(category=category).count()
        print(f"{category.name}: {count} items")

if __name__ == '__main__':
    pdf_path = 'Menu (2).pdf'  # Make sure PDF is in the same directory
    
    if os.path.exists(pdf_path):
        import_menu_from_pdf(pdf_path)
    else:
        print(f"PDF file not found: {pdf_path}")
        print("\nPlease save 'Menu (2).pdf' in the project directory:")
        print("C:\\restaurant_pos\\Menu (2).pdf")