from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_order_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-total_spent']
    
    def __str__(self):
        return f"{self.name} ({self.phone})"
    
    def update_stats(self):
        from pos.models import Order
        orders = Order.objects.filter(customer_phone=self.phone, status='completed')
        self.total_orders = orders.count()
        self.total_spent = sum(float(order.total) for order in orders)
        
        last_order = orders.order_by('-created_at').first()
        if last_order:
            self.last_order_date = last_order.created_at
        
        self.save()