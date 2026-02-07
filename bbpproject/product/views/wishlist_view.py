from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib import messages
from ..models import Product, Wishlist, Cart, CartItem
from .cart_detail_view import get_or_create_cart

class WishlistView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "pages/product/wishlist.html"
    context_object_name = "wishlist_items"

    def get_queryset(self):
        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)
        return wishlist.products.all()

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        added = False
        message = "Removed from wishlist"
    else:
        wishlist.products.add(product)
        added = True
        message = "Added to wishlist"
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'added': added,
            'message': message,
            'wishlist_count': wishlist.products.count()
        })
    
    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'product:product_list'))

@login_required
def wishlist_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    # Check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Remove from wishlist
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"{product.name} moved to cart",
            'cart_count': cart.items.count(),
            'wishlist_count': wishlist.products.count()
        })
    
    messages.success(request, f"{product.name} moved to cart")
    return redirect('product:wishlist_detail')

@login_required
def wishlist_add_all_to_cart(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    cart = get_or_create_cart(request)
    
    products = wishlist.products.all()
    count = products.count()
    
    if count == 0:
        messages.info(request, "Your wishlist is empty.")
        return redirect('product:wishlist_detail')
        
    for product in products:
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            
    # Clear wishlist
    wishlist.products.clear()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"{count} items moved to cart",
            'cart_count': cart.items.count(),
            'wishlist_count': 0
        })
        
    messages.success(request, f"{count} items moved to cart")
    return redirect('product:cart_detail')
