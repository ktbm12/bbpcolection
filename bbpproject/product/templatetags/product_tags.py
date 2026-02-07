from django import template
from ..models import Wishlist

register = template.Library()

@register.filter
def is_in_wishlist(product, user):
    if not user.is_authenticated:
        return False
    try:
        wishlist = Wishlist.objects.get(user=user)
        return wishlist.products.filter(id=product.id).exists()
    except Wishlist.DoesNotExist:
        return False
