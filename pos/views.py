from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

def home(request):
    # Create tables if they don't exist
    if not Table.objects.exists():
        for i in range(1, 11):
            Table.objects.create(
                table_number=str(i),
                table_name=f"Table {i}",
                capacity=4 if i <= 6 else 6
            )
    
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
        
        order, created = Order.objects.get_or_create(
            table=table,
            status='active',
            defaults={'subtotal': 0, 'total': 0}
        )
        
        existing_item = order.order_items.filter(menu_item=menu_item).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price=menu_item.price
            )
        
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
            OrderItem.objects.filter(id=item_id).delete()
        else:
            item = OrderItem.objects.get(id=item_id)
            item.quantity = quantity
            item.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

def generate_bill(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'cash')
        paid_amount = float(request.POST.get('paid_amount', order.total))
        customer_name = request.POST.get('customer_name', '')
        customer_phone = request.POST.get('customer_phone', '')
        
        order.customer_name = customer_name
        order.customer_phone = customer_phone
        order.save()
        
        bill = Bill.objects.create(
            order=order,
            payment_method=payment_method,
            paid_amount=paid_amount
        )
        
        return redirect('print_bill', bill_id=bill.id)
    
    context = {'order': order}
    return render(request, 'pos/generate_bill.html', context)

def print_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    context = {'bill': bill}
    return render(request, 'pos/print_bill.html', context)