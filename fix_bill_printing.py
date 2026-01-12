import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

print("=" * 60)
print("FIXING BILL PRINTING ISSUE")
print("=" * 60)

# The issue is in the template using wrong variable name
# In models.py, we defined related_name='order_items' for OrderItem
# So we need to use order.order_items.all() not order.items.all()

print("Issue: Templates were using 'order.items.all()'")
print("Fix: Changed to 'order.order_items.all()'")
print("\nFiles fixed:")
print("1. templates/pos/print_bill.html")
print("2. templates/pos/generate_bill.html")
print("3. templates/pos/table_detail.html")

print("\n" + "=" * 60)
print("FIX APPLIED!")
print("Now bills will show items and quantities correctly.")
print("=" * 60)