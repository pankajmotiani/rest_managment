from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Customer
from pos.models import Order

@login_required
def customers_list(request):
    search = request.GET.get('search', '')
    
    if search:
        customers = Customer.objects.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search)
        ).order_by('-total_spent')
    else:
        customers = Customer.objects.all().order_by('-total_spent')
    
    # Update stats for all customers
    for customer in customers:
        customer.update_stats()
    
    context = {
        'customers': customers,
        'search': search,
    }
    return render(request, 'customers/list.html', context)

@login_required
def customer_detail(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    orders = Order.objects.filter(customer_phone=customer.phone).order_by('-created_at')
    
    # Calculate favorite items
    from django.db.models import Count
    favorite_items = Order.objects.filter(
        customer_phone=customer.phone
    ).values(
        'order_items__menu_item__name'
    ).annotate(
        count=Count('order_items__menu_item__name')
    ).order_by('-count')[:5]
    
    context = {
        'customer': customer,
        'orders': orders,
        'favorite_items': favorite_items,
    }
    return render(request, 'customers/detail.html', context)

@login_required
def sync_customers(request):
    # Sync customers from orders
    orders_with_customers = Order.objects.filter(
        customer_phone__isnull=False
    ).exclude(customer_phone='')
    
    for order in orders_with_customers:
        customer, created = Customer.objects.get_or_create(
            phone=order.customer_phone,
            defaults={
                'name': order.customer_name or f"Customer {order.customer_phone}",
                'email': ''
            }
        )
        customer.update_stats()
    
    return redirect('customers_list')