from django.utils import timezone
from .models import Promotion

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
