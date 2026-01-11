from .models import Restaurant

def restaurant_info(request):
    """Add restaurant info to all templates"""
    restaurant = Restaurant.objects.first()
    return {
        'restaurant': restaurant if restaurant else Restaurant(),
        'now': '2024-01-10',  # You can replace with actual datetime
    }