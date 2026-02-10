# product/context_processors.py
from .views.cart_detail_view import get_or_create_cart, get_cart_summary
from .views.wishlist_view import get_wishlist_count

def cart_counter(request):
    """
    Rend le nombre d'articles du panier et de la wishlist disponible dans tous les templates.
    """
    context = {
        'cart_items_count': 0,
        'wishlist_count': 0
    }
    
    # Cart count (works for auth and guest now)
    cart = get_or_create_cart(request)
    if cart:
        summary = get_cart_summary(cart)
        context['cart_items_count'] = summary.get('cart_items_count', 0)
    
    # Wishlist count
    context['wishlist_count'] = get_wishlist_count(request)
        
    return context
