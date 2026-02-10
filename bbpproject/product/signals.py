from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem, Wishlist, Product

@receiver(user_logged_in)
def merge_cart_and_wishlist(sender, user, request, **kwargs):
    # 1. Merge Cart
    cart_id = request.session.get('cart_id')
    session_cart = None
    
    if cart_id:
        session_cart = Cart.objects.filter(id=cart_id, user__isnull=True).first()
    elif request.session.session_key:
        # Fallback to current session key if no custom cart_id
        session_cart = Cart.objects.filter(session_key=request.session.session_key, user__isnull=True).first()
        
    if session_cart:
        user_cart, created = Cart.objects.get_or_create(user=user)
        
        # Move items
        for item in session_cart.items.all():
            user_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
            if not created:
                user_item.quantity += item.quantity
                user_item.save()
            else:
                user_item.quantity = item.quantity
                user_item.save()
        
        # Delete session cart
        session_cart.delete()
        if 'cart_id' in request.session:
            del request.session['cart_id']
            request.session.modified = True
            
    # 2. Merge Wishlist
    wishlist_ids = request.session.get('wishlist_ids', [])
    if wishlist_ids:
        user_wishlist, created = Wishlist.objects.get_or_create(user=user)
        products = Product.objects.filter(id__in=wishlist_ids)
        for product in products:
            user_wishlist.products.add(product)
            
        # Clear session
        del request.session['wishlist_ids']
        request.session.modified = True
