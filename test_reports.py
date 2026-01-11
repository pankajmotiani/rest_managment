import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
import django
django.setup()

# Test if views can be imported
try:
    from reports.views import sales_dashboard, export_report, item_sales_report
    print("✅ Views imported successfully!")
    
    # Check URLs
    from django.urls import reverse
    try:
        reverse('sales_dashboard')
        print("✅ URLs configured correctly!")
    except Exception as e:
        print(f"❌ URL error: {e}")
        
except Exception as e:
    print(f"❌ Import error: {e}")

# Check if templates exist
import os
if os.path.exists('templates/reports/dashboard.html'):
    print("✅ Template exists!")
else:
    print("❌ Template not found at: templates/reports/dashboard.html")