from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import InventorySettings, Ingredient, InventoryTransaction
from django.utils import timezone
from datetime import timedelta

@login_required
def inventory_dashboard(request):
    """Inventory dashboard"""
    try:
        settings, created = InventorySettings.objects.get_or_create(id=1)
        
        ingredients = Ingredient.objects.filter(is_active=True)
        
        # Calculate statistics
        total_ingredients = ingredients.count()
        low_stock = ingredients.filter(current_stock__lte=models.F('minimum_stock')).count()
        out_of_stock = ingredients.filter(current_stock=0).count()
        
        # Recent transactions
        recent_transactions = InventoryTransaction.objects.all().order_by('-created_at')[:10]
        
        # Low stock items
        low_stock_items = ingredients.filter(current_stock__lte=models.F('minimum_stock'))
        
        context = {
            'settings': settings,
            'total_ingredients': total_ingredients,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'recent_transactions': recent_transactions,
            'low_stock_items': low_stock_items,
            'ingredients': ingredients,
        }
        
        return render(request, 'inventory/dashboard.html', context)
        
    except Exception as e:
        return render(request, 'inventory/error.html', {'error': str(e)})

@login_required
def update_stock(request, ingredient_id):
    """Update ingredient stock"""
    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
        
        if request.method == 'POST':
            transaction_type = request.POST.get('transaction_type')
            quantity = Decimal(request.POST.get('quantity', 0))
            notes = request.POST.get('notes', '')
            
            if transaction_type and quantity > 0:
                InventoryTransaction.objects.create(
                    ingredient=ingredient,
                    transaction_type=transaction_type,
                    quantity=quantity,
                    reference="Manual Update",
                    notes=notes,
                    created_by=request.user
                )
            
            return redirect('inventory_dashboard')
        
        return redirect('inventory_dashboard')
        
    except Exception as e:
        return render(request, 'inventory/error.html', {'error': str(e)})

@login_required
def toggle_inventory(request):
    """Enable/disable inventory"""
    try:
        settings = InventorySettings.objects.first()
        if not settings:
            settings = InventorySettings.objects.create()
        
        settings.is_enabled = not settings.is_enabled
        settings.save()
        
        return redirect('inventory_dashboard')
        
    except Exception as e:
        return render(request, 'inventory/error.html', {'error': str(e)})