from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer

@login_required
def customers_list(request):
    """List all customers"""
    try:
        customers = Customer.objects.all().order_by('-total_spent')
        
        # Update stats for each customer
        for customer in customers:
            customer.update_stats()
        
        context = {
            'customers': customers,
        }
        return render(request, 'customers/list.html', context)
        
    except Exception as e:
        return render(request, 'customers/error.html', {'error': str(e)})

@login_required
def customer_detail(request, customer_id):
    """View customer details"""
    try:
        from pos.models import Order
        
        customer = Customer.objects.get(id=customer_id)
        orders = Order.objects.filter(customer_phone=customer.phone, status='completed').order_by('-created_at')
        
        context = {
            'customer': customer,
            'orders': orders,
        }
        return render(request, 'customers/detail.html', context)
        
    except Exception as e:
        return render(request, 'customers/error.html', {'error': str(e)})

@login_required
def sync_customers(request):
    """Sync customers from orders"""
    try:
        from pos.models import Order
        
        orders = Order.objects.filter(status='completed').exclude(customer_phone='')
        
        for order in orders:
            if order.customer_phone:
                customer, created = Customer.objects.get_or_create(
                    phone=order.customer_phone,
                    defaults={
                        'name': order.customer_name or f"Customer {order.customer_phone}",
                        'email': ''
                    }
                )
                customer.update_stats()
        
        return redirect('customers_list')
        
    except Exception as e:
        return render(request, 'customers/error.html', {'error': str(e)})