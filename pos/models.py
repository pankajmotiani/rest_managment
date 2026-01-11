from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=200, default="KAKA CAFE")
    address = models.TextField(default="Bangalore")
    phone = models.CharField(max_length=20, default="7022470962")
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menuitems')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category__display_order', 'name']
    
    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    table_name = models.CharField(max_length=50, blank=True)
    capacity = models.IntegerField(default=4)
    status = models.CharField(max_length=20, default='available', 
                             choices=[('available', 'Available'), 
                                     ('occupied', 'Occupied')])
    
    def __str__(self):
        return f"Table {self.table_number}"

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=200, blank=True)
    customer_phone = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=20, default='active',
                             choices=[('active', 'Active'), 
                                     ('completed', 'Completed')])
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def calculate_totals(self):
        items_total = sum(item.total for item in self.order_items.all())
        self.subtotal = items_total
        self.total = items_total - self.discount
        self.save()
    
    def __str__(self):
        return f"Order #{self.id} - Table {self.table.table_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        self.price = self.menu_item.price
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)
        self.order.calculate_totals()
    
    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

class Bill(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='bill')
    bill_number = models.CharField(max_length=20, unique=True)
    payment_method = models.CharField(max_length=50, 
                                     choices=[('cash', 'Cash'), 
                                             ('card', 'Card'),
                                             ('upi', 'UPI')],
                                     default='cash')
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    change_return = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.bill_number:
            import datetime
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            last_bill = Bill.objects.filter(bill_number__startswith=date_str).count()
            self.bill_number = f"{date_str}{last_bill + 1:04d}"
        
        if self.paid_amount > self.order.total:
            self.change_return = self.paid_amount - self.order.total
        else:
            self.change_return = 0
        
        self.order.status = 'completed'
        self.order.save()
        
        self.order.table.status = 'available'
        self.order.table.save()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Bill {self.bill_number}"