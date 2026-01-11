from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import csv

@login_required
def sales_dashboard(request):
    from pos.models import Bill, Order
    
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_start = today.replace(day=1)
    
    # Get all bills
    all_bills = Bill.objects.all()
    
    # Today's sales
    today_bills = [b for b in all_bills if b.created_at.date() == today]
    daily_total = sum(float(b.order.total) for b in today_bills)
    daily_count = len(today_bills)
    daily_avg = daily_total / daily_count if daily_count > 0 else 0
    
    # Weekly sales
    weekly_bills = [b for b in all_bills if b.created_at.date() >= week_ago]
    weekly_total = sum(float(b.order.total) for b in weekly_bills)
    weekly_count = len(weekly_bills)
    
    # Monthly sales
    monthly_bills = [b for b in all_bills if b.created_at.date() >= month_start]
    monthly_total = sum(float(b.order.total) for b in monthly_bills)
    monthly_count = len(monthly_bills)
    
    # Top items
    top_items = []
    if weekly_bills:
        items_dict = {}
        for bill in weekly_bills:
            for item in bill.order.order_items.all():
                name = item.menu_item.name
                if name not in items_dict:
                    items_dict[name] = {'quantity': 0, 'revenue': 0}
                items_dict[name]['quantity'] += item.quantity
                items_dict[name]['revenue'] += float(item.total)
        
        items_list = [{'name': k, 'quantity': v['quantity'], 'revenue': v['revenue']} 
                     for k, v in items_dict.items()]
        items_list.sort(key=lambda x: x['revenue'], reverse=True)
        top_items = items_list[:10]
    
    context = {
        'today': today,
        'daily_sales': daily_total,
        'daily_orders': daily_count,
        'daily_avg': daily_avg,
        'weekly_sales': weekly_total,
        'weekly_orders': weekly_count,
        'monthly_sales': monthly_total,
        'monthly_orders': monthly_count,
        'top_items': top_items,
        'recent_bills': all_bills.order_by('-created_at')[:10],
    }
    
    return render(request, 'reports/dashboard.html', context)

@login_required
def export_report(request, report_type):
    from pos.models import Bill
    
    today = timezone.now().date()
    
    if report_type == 'daily':
        bills = Bill.objects.filter(created_at__date=today)
        filename = f"daily_report_{today}.csv"
    elif report_type == 'weekly':
        week_ago = today - timedelta(days=7)
        bills = Bill.objects.filter(created_at__date__gte=week_ago)
        filename = f"weekly_report_{today}.csv"
    else:
        bills = Bill.objects.all()
        filename = f"complete_report_{today}.csv"
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['Bill No', 'Date', 'Table', 'Customer', 'Total', 'Payment'])
    
    for bill in bills:
        writer.writerow([
            bill.bill_number,
            bill.created_at.strftime('%Y-%m-%d %H:%M'),
            bill.order.table.table_number,
            bill.order.customer_name or 'Walk-in',
            f"₹{bill.order.total:.2f}",
            bill.payment_method,
        ])
    
    return response

@login_required
def item_sales_report(request):
    from pos.models import Bill
    
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    weekly_bills = Bill.objects.filter(created_at__date__gte=week_ago)
    
    items_dict = {}
    total_quantity = 0
    total_revenue = 0
    
    for bill in weekly_bills:
        for item in bill.order.order_items.all():
            name = item.menu_item.name
            if name not in items_dict:
                items_dict[name] = {'quantity': 0, 'revenue': 0}
            items_dict[name]['quantity'] += item.quantity
            items_dict[name]['revenue'] += float(item.total)
            total_quantity += item.quantity
            total_revenue += float(item.total)
    
    items_list = [{'name': k, 'quantity': v['quantity'], 'revenue': v['revenue']} 
                 for k, v in items_dict.items()]
    items_list.sort(key=lambda x: x['revenue'], reverse=True)
    
    context = {
        'items': items_list,
        'start_date': week_ago,
        'end_date': today,
        'total_quantity': total_quantity,
        'total_revenue': total_revenue,
    }
    
    return render(request, 'reports/item_sales.html', context)