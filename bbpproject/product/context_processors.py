from .views.cart_detail_view import get_or_create_cart, get_cart_summary

def cart_counter(request):
    """
    Rend le nombre d'articles du panier disponible dans tous les templates.
    """
    if request.user.is_authenticated:
        cart = get_or_create_cart(request)
        if cart:
            summary = get_cart_summary(cart)
            return {'cart_items_count': summary.get('cart_items_count', 0)}
    return {'cart_items_count': 0}
