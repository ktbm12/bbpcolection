from .views.cart_detail_view import get_or_create_cart, get_cart_summary
from .models import Wishlist

def cart_counter(request):
    """
    Rend le nombre d'articles du panier et de la wishlist disponible dans tous les templates.
    """
    context = {
        'cart_items_count': 0,
        'wishlist_count': 0
    }
    
    if request.user.is_authenticated:
        # Cart count
        cart = get_or_create_cart(request)
        if cart:
            summary = get_cart_summary(cart)
            context['cart_items_count'] = summary.get('cart_items_count', 0)
        
        # Wishlist count
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        context['wishlist_count'] = wishlist.products.count()
        
    return context
