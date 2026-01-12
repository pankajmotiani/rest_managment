from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from pos.models import Order, Bill
from decimal import Decimal
import json

@login_required
def inventory_dashboard(request):
    settings = InventorySettings.objects.first()
    if not settings:
        settings = InventorySettings.objects.create()
    
    ingredients = Ingredient.objects.filter(is_active=True)
    low_stock = ingredients.filter(current_stock__lte=models.F('minimum_stock'))
    
    # Recent transactions
    recent_transactions = InventoryTransaction.objects.all().order_by('-created_at')[:20]
    
    # Menu items without recipes
    from pos.models import MenuItem
    menu_items_without_recipes = MenuItem.objects.exclude(recipes__isnull=False).count()
    
    context = {
        'settings': settings,
        'ingredients': ingredients,
        'low_stock_count': low_stock.count(),
        'low_stock_items': low_stock,
        'recent_transactions': recent_transactions,
        'menu_items_without_recipes': menu_items_without_recipes,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def toggle_inventory(request):
    settings = InventorySettings.objects.first()
    if not settings:
        settings = InventorySettings.objects.create()
    
    if request.method == 'POST':
        settings.is_enabled = not settings.is_enabled
        settings.save()
    
    return redirect('inventory_dashboard')

@login_required
def ingredient_detail(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    transactions = ingredient.transactions.all().order_by('-created_at')
    
    context = {
        'ingredient': ingredient,
        'transactions': transactions,
    }
    return render(request, 'inventory/ingredient_detail.html', context)

@login_required
def update_stock(request, ingredient_id):
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
                reference=request.POST.get('reference', ''),
                notes=notes
            )
    
    return redirect('ingredient_detail', ingredient_id=ingredient_id)

@login_required
def recipe_management(request):
    from pos.models import MenuItem
    menu_items = MenuItem.objects.all()
    ingredients = Ingredient.objects.filter(is_active=True)
    
    context = {
        'menu_items': menu_items,
        'ingredients': ingredients,
    }
    return render(request, 'inventory/recipe_management.html', context)

@login_required
def create_recipe(request):
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item')
        ingredient_data = json.loads(request.POST.get('ingredients', '[]'))
        
        menu_item = MenuItem.objects.get(id=menu_item_id)
        
        # Create or get recipe
        recipe, created = Recipe.objects.get_or_create(menu_item=menu_item)
        
        # Clear existing ingredients
        recipe.ingredients.clear()
        
        # Add new ingredients
        for item in ingredient_data:
            ingredient = Ingredient.objects.get(id=item['id'])
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity_required=Decimal(item['quantity'])
            )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

def auto_update_inventory(order_id):
    """Auto update inventory when bill is generated"""
    try:
        settings = InventorySettings.objects.first()
        if not settings or not settings.is_enabled or not settings.auto_update_on_bill:
            return False
        
        order = Order.objects.get(id=order_id)
        
        for order_item in order.order_items.all():
            try:
                recipe = order_item.menu_item.recipes.first()
                if recipe:
                    for recipe_ingredient in recipe.recipeingredient_set.all():
                        # Calculate consumption
                        consumption = recipe_ingredient.quantity_required * order_item.quantity
                        
                        InventoryTransaction.objects.create(
                            ingredient=recipe_ingredient.ingredient,
                            transaction_type='consumption',
                            quantity=consumption,
                            reference=f"Order #{order.id} - {order_item.menu_item.name}",
                            notes=f"Auto consumption for {order_item.quantity} x {order_item.menu_item.name}"
                        )
            except:
                continue
        
        return True
    except:
        return False

@login_required
def inventory_reports(request):
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    
    # Date ranges
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Consumption report
    consumption_data = InventoryTransaction.objects.filter(
        transaction_type='consumption',
        created_at__date__gte=month_ago
    ).values('ingredient__name').annotate(
        total_consumed=Sum('quantity')
    ).order_by('-total_consumed')
    
    # Low stock report
    low_stock = Ingredient.objects.filter(
        current_stock__lte=models.F('minimum_stock'),
        is_active=True
    )
    
    context = {
        'consumption_data': consumption_data,
        'low_stock': low_stock,
        'today': today,
        'week_ago': week_ago,
        'month_ago': month_ago,
    }
    return render(request, 'inventory/reports.html', context)