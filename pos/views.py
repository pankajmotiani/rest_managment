from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
import json
from decimal import Decimal

def home(request):
    tables = Table.objects.all()
    categories = Category.objects.all()
    
    context = {
        'tables': tables,
        'categories': categories,
    }
    return render(request, 'pos/home.html', context)

def table_detail(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    order = Order.objects.filter(table=table, status='active').first()
    categories = Category.objects.all()
    
    context = {
        'table': table,
        'order': order,
        'categories': categories,
    }
    return render(request, 'pos/table_detail.html', context)

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        table_id = data.get('table_id')
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        table = Table.objects.get(id=table_id)
        menu_item = MenuItem.objects.get(id=item_id)
        
        # Get or create active order for table
        order, created = Order.objects.get_or_create(
            table=table,
            status='active'
        )
        
        # Check if item already exists in order
        existing_item = order.order_items.filter(menu_item=menu_item).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity
            )
        
        # Update table status
        table.status = 'occupied'
        table.save()
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'total': float(order.total)
        })
    
    return JsonResponse({'success': False})

@csrf_exempt
def update_item_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 0))
        
        if quantity <= 0:
            # Delete item if quantity is 0 or negative
            OrderItem.objects.filter(id=item_id).delete()
        else:
            item = OrderItem.objects.get(id=item_id)
            item.quantity = quantity
            item.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@csrf_exempt
def update_charges(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        order = Order.objects.get(id=order_id)
        
        # Update charges (NO TAX)
        order.water_bottle = Decimal(data.get('water_bottle', 0))
        order.packaging = Decimal(data.get('packaging', 0))
        order.service_charge = Decimal(data.get('service_charge', 0))
        order.other_charges = Decimal(data.get('other_charges', 0))
        order.other_charges_description = data.get('other_charges_description', '')
        order.discount = Decimal(data.get('discount', 0))
        
        order.save()
        
        return JsonResponse({
            'success': True,
            'total': float(order.total),
            'subtotal': float(order.subtotal)
        })
    
    return JsonResponse({'success': False})

def generate_bill(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'cash')
        paid_amount = Decimal(request.POST.get('paid_amount', order.total))
        customer_name = request.POST.get('customer_name', order.customer_name)
        customer_phone = request.POST.get('customer_phone', order.customer_phone)
        
        # Update order with customer details
        order.customer_name = customer_name
        order.customer_phone = customer_phone
        order.save()
        
        # Create bill
        bill = Bill.objects.create(
            order=order,
            payment_method=payment_method,
            paid_amount=paid_amount
        )
        
        # Mark order as completed
        order.status = 'completed'
        order.save()
        
        # Free up table
        table = order.table
        table.status = 'available'
        table.save()
        
        return redirect('print_bill', bill_id=bill.id)
    
    context = {
        'order': order,
    }
    return render(request, 'pos/generate_bill.html', context)

def print_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    
    context = {
        'bill': bill,
        'order': bill.order,
    }
    return render(request, 'pos/print_bill.html', context)