from django.utils import timezone
from django.db.models import Sum
from .models import Promotion
from .views.cart_detail_view import get_or_create_cart

def active_promotion(request):
    """
    Returns the currently active promotion and its items.
    """
    now = timezone.now()
    active_promo = Promotion.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    ).prefetch_related('items', 'items__product').first()
    
    return {
        'active_promo': active_promo
    }

def cart_counter(request):
    """
    Exposes the number of items in the current user's cart.
    """
    cart = get_or_create_cart(request)
    count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    return {
        'cart_count': count
    }
