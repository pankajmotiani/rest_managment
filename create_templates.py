import os

# Create templates directory
os.makedirs('templates/pos', exist_ok=True)

# Template files content
templates = {
    'generate_bill.html': """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generate Bill - {{ restaurant.name }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <div class="bg-white rounded-xl shadow-lg p-6">
            <h1 class="text-2xl font-bold mb-6">Generate Bill for Table {{ order.table.table_number }}</h1>
            
            <!-- Simple bill preview -->
            <div class="bg-gray-50 p-4 rounded-lg mb-6">
                <h3 class="font-bold text-lg mb-3">Order Summary</h3>
                {% for item in order.items.all %}
                <div class="flex justify-between py-2 border-b">
                    <span>{{ item.menu_item.name }} x {{ item.quantity }}</span>
                    <span>₹{{ item.total }}</span>
                </div>
                {% endfor %}
                
                <div class="mt-4">
                    <div class="flex justify-between py-1">
                        <span>Subtotal:</span>
                        <span>₹{{ order.subtotal }}</span>
                    </div>
                    <div class="flex justify-between py-1">
                        <span>Tax ({{ order.tax_rate }}%):</span>
                        <span>₹{{ order.tax_amount }}</span>
                    </div>
                    <div class="flex justify-between py-1">
                        <span>Extra Charges:</span>
                        <span>₹{{ order.water_bottle|add:order.packaging|add:order.service_charge|add:order.other_charges }}</span>
                    </div>
                    {% if order.discount > 0 %}
                    <div class="flex justify-between py-1 text-red-600">
                        <span>Discount:</span>
                        <span>-₹{{ order.discount }}</span>
                    </div>
                    {% endif %}
                    <div class="flex justify-between py-2 mt-2 border-t font-bold text-lg">
                        <span>TOTAL:</span>
                        <span class="text-green-600">₹{{ order.total }}</span>
                    </div>
                </div>
            </div>
            
            <!-- Payment form -->
            <form method="post">
                {% csrf_token %}
                <div class="mb-4">
                    <label class="block font-medium mb-2">Payment Method</label>
                    <select name="payment_method" class="w-full border rounded-lg px-4 py-2" required>
                        <option value="cash">Cash</option>
                        <option value="card">Card</option>
                        <option value="upi">UPI</option>
                    </select>
                </div>
                
                <div class="mb-4">
                    <label class="block font-medium mb-2">Amount Received</label>
                    <input type="number" name="paid_amount" value="{{ order.total }}" 
                           class="w-full border rounded-lg px-4 py-2" required>
                </div>
                
                <div class="flex gap-4">
                    <button type="submit" class="bg-green-500 text-white px-6 py-3 rounded-lg font-bold">
                        Generate Bill
                    </button>
                    <a href="{% url 'table_detail' order.table.id %}" class="bg-gray-500 text-white px-6 py-3 rounded-lg font-bold">
                        Back to Order
                    </a>
                </div>
            </form>
        </div>
    </div>
</body>
</html>""",
    
    'print_bill.html': """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bill {{ bill.bill_number }}</title>
    <style>
        body { font-family: monospace; }
        @media print { .no-print { display: none; } }
    </style>
</head>
<body onload="window.print()">
    <div style="max-width: 300px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 15px;">
            <h2 style="font-weight: bold;">{{ restaurant.name }}</h2>
            <p style="font-size: 12px;">{{ restaurant.address }}</p>
            <p style="font-size: 12px;">{{ restaurant.phone }}</p>
        </div>
        
        <div style="text-align: center; margin: 15px 0;">
            <h3>TAX INVOICE</h3>
            <p>Bill No: {{ bill.bill_number }}</p>
            <p>Date: {{ bill.created_at|date:"d/m/Y H:i" }}</p>
        </div>
        
        <table style="width: 100%; margin: 15px 0;">
            <thead>
                <tr>
                    <th style="text-align: left;">Item</th>
                    <th style="text-align: center;">Qty</th>
                    <th style="text-align: right;">Price</th>
                </tr>
            </thead>
            <tbody>
                {% for item in bill.order.items.all %}
                <tr>
                    <td>{{ item.menu_item.name }}</td>
                    <td style="text-align: center;">{{ item.quantity }}</td>
                    <td style="text-align: right;">₹{{ item.total }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <div style="border-top: 2px dashed #000; padding-top: 10px;">
            <div style="display: flex; justify-content: space-between;">
                <span>Subtotal:</span>
                <span>₹{{ bill.order.subtotal }}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Tax:</span>
                <span>₹{{ bill.order.tax_amount }}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-weight: bold; margin-top: 10px;">
                <span>TOTAL:</span>
                <span>₹{{ bill.order.total }}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <span>Paid:</span>
                <span>₹{{ bill.paid_amount }}</span>
            </div>
            {% if bill.change_return > 0 %}
            <div style="display: flex; justify-content: space-between;">
                <span>Change:</span>
                <span>₹{{ bill.change_return }}</span>
            </div>
            {% endif %}
        </div>
        
        <div style="text-align: center; margin-top: 20px; padding-top: 10px; border-top: 1px dashed #000;">
            <p>Thank you for dining with us!</p>
            <p style="font-size: 10px;">{{ restaurant.name }}</p>
        </div>
    </div>
    
    <div class="no-print" style="text-align: center; margin-top: 20px;">
        <button onclick="window.print()">Print Again</button>
        <a href="{% url 'home' %}" style="margin-left: 10px;">Home</a>
    </div>
</body>
</html>"""
}

# Write templates to files
for filename, content in templates.items():
    filepath = f'templates/pos/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {filepath}')

print('\nAll templates created successfully!')