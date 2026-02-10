from django import template
from ..models import Wishlist

register = template.Library()

@register.filter
def is_in_wishlist(product, request):
    # Check if we got a user object instead of request (legacy support or mistake)
    if hasattr(request, 'user'):
        user = request.user
        session = request.session
    else:
        # Fallback if someone passed just user and it's authenticated
        if hasattr(request, 'is_authenticated') and request.is_authenticated:
            try:
                wishlist = Wishlist.objects.get(user=request)
                return wishlist.products.filter(id=product.id).exists()
            except Wishlist.DoesNotExist:
                return False
        return False

    if user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=user)
            return wishlist.products.filter(id=product.id).exists()
        except Wishlist.DoesNotExist:
            return False
    else:
        # Guest user - check session
        wishlist_ids = session.get('wishlist_ids', [])
        return str(product.id) in wishlist_ids
