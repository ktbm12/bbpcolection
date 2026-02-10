from celery import shared_task
from django.conf import settings
from product.models import Product
from core.email_utils import send_templated_email
from django.db.models import F

@shared_task
def check_low_stock_task():
    """
    Check for products with low stock and notify admin.
    """
    LOW_STOCK_THRESHOLD = 5
    low_stock_products = Product.objects.filter(stock__lte=LOW_STOCK_THRESHOLD, is_active=True)
    
    if low_stock_products.exists():
        admin_email = settings.ADMINS[0][1] if settings.ADMINS else None
        if admin_email:
            context = {
                'products': low_stock_products,
                'threshold': LOW_STOCK_THRESHOLD
            }
            send_templated_email(
                subject="⚠️ Alerte Stock Faible - bbpcollection",
                to_email=admin_email,
                template_name='emails/admin_low_stock.html',
                context=context
            )
        return f"Notified admin about {low_stock_products.count()} products."
    return "No low stock products found."
