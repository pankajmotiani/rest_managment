from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import datetime, timedelta
from pos.models import Order, OrderItem, Bill
import json

@login_required
def sales_dashboard(request):
    today = timezone.now().date()
    
    # Daily Report
    daily_sales = Bill.objects.filter(
        created_at__date=today
    ).aggregate(
        total_sales=Sum('order__total'),
        total_orders=Count('id'),
        avg_order=Sum('order__total') / Count('id')
    )
    
    # Weekly Report (last 7 days)
    week_ago = today - timedelta(days=7)
    weekly_sales = Bill.objects.filter(
        created_at__date__gte=week_ago
    ).aggregate(
        total_sales=Sum('order__total'),
        total_orders=Count('id')
    )
    
    # Monthly Report (current month)
    month_start = today.replace(day=1)
    monthly_sales = Bill.objects.filter(
        created_at__date__gte=month_start
    ).aggregate(
        total_sales=Sum('order__total'),
        total_orders=Count('id')
    )
    
    # Top Selling Items (last 7 days)
    top_items = OrderItem.objects.filter(
        order__bill__created_at__date__gte=week_ago
    ).values(
        'menu_item__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('total')
    ).order_by('-total_quantity')[:10]
    
    # Sales by Hour (today)
    hourly_sales = Bill.objects.filter(
        created_at__date=today
    ).extra({
        'hour': "EXTRACT(HOUR FROM created_at)"
    }).values('hour').annotate(
        sales=Sum('order__total'),
        orders=Count('id')
    ).order_by('hour')
    
    # Format hourly data for chart
    hourly_labels = []
    hourly_data = []
    for hour in range(9, 24):  # 9 AM to 11 PM (restaurant hours)
        hour_data = next((h for h in hourly_sales if h['hour'] == hour), {'sales': 0})
        hourly_labels.append(f"{hour}:00")
        hourly_data.append(float(hour_data['sales'] or 0))
    
    context = {
        'today': today,
        'daily_sales': daily_sales['total_sales'] or 0,
        'daily_orders': daily_sales['total_orders'] or 0,
        'daily_avg': daily_sales['avg_order'] or 0,
        'weekly_sales': weekly_sales['total_sales'] or 0,
        'weekly_orders': weekly_sales['total_orders'] or 0,
        'monthly_sales': monthly_sales['total_sales'] or 0,
        'monthly_orders': monthly_sales['total_orders'] or 0,
        'top_items': top_items,
        'hourly_labels': json.dumps(hourly_labels),
        'hourly_data': json.dumps(hourly_data),
    }
    
    return render(request, 'reports/dashboard.html', context)

@login_required
def export_report(request, report_type):
    from django.http import HttpResponse
    import csv
    from io import StringIO
    
    today = timezone.now().date()
    
    if report_type == 'daily':
        bills = Bill.objects.filter(created_at__date=today)
        filename = f"daily_report_{today}.csv"
    elif report_type == 'weekly':
        week_ago = today - timedelta(days=7)
        bills = Bill.objects.filter(created_at__date__gte=week_ago)
        filename = f"weekly_report_{today}.csv"
    elif report_type == 'monthly':
        month_start = today.replace(day=1)
        bills = Bill.objects.filter(created_at__date__gte=month_start)
        filename = f"monthly_report_{today}.csv"
    else:
        bills = Bill.objects.all()
        filename = f"complete_report_{today}.csv"
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['Bill No', 'Date', 'Table', 'Customer', 'Items', 'Subtotal', 'Discount', 'Total', 'Payment Method'])
    
    for bill in bills:
        items = ", ".join([f"{item.menu_item.name} x{item.quantity}" for item in bill.order.order_items.all()])
        writer.writerow([
            bill.bill_number,
            bill.created_at.strftime('%Y-%m-%d %H:%M'),
            bill.order.table.table_number,
            bill.order.customer_name or 'Walk-in',
            items,
            bill.order.subtotal,
            bill.order.discount,
            bill.order.total,
            bill.get_payment_method_display()
        ])
    
    return response

@login_required
def item_sales_report(request):
    from datetime import datetime, timedelta
    
    period = request.GET.get('period', 'week')
    today = timezone.now().date()
    
    if period == 'today':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=7)
        end_date = today
    elif period == 'month':
        start_date = today.replace(day=1)
        end_date = today
    else:
        start_date = today - timedelta(days=365)
        end_date = today
    
    items = OrderItem.objects.filter(
        order__bill__created_at__date__range=[start_date, end_date]
    ).values(
        'menu_item__name',
        'menu_item__category__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('total')
    ).order_by('-total_quantity')
    
    context = {
        'items': items,
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'reports/item_sales.html', context)