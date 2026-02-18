from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.contrib import messages
from ..models import Product, Wishlist, Cart, CartItem
from .cart_detail_view import get_or_create_cart

def get_wishlist_products(request):
    """
    Helper to get wishlist products whether authenticated or not.
    """
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        return wishlist.products.all()
    else:
        wishlist_ids = request.session.get('wishlist_ids', [])
        if not wishlist_ids:
            return Product.objects.none()
        return Product.objects.filter(id__in=wishlist_ids, is_active=True)

def get_wishlist_count(request):
    """Helper to get count"""
    if request.user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        return wishlist.products.count()
    else:
        return len(request.session.get('wishlist_ids', []))

class WishlistView(ListView):
    model = Product
    template_name = "pages/product/wishlist.html"
    context_object_name = "wishlist_items"

    def get_queryset(self):
        return get_wishlist_products(self.request)

class ToggleWishlistView(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        added = False
        
        if request.user.is_authenticated:
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            if product in wishlist.products.all():
                wishlist.products.remove(product)
                message = "Removed from wishlist"
            else:
                wishlist.products.add(product)
                added = True
                message = "Added to wishlist"
            count = wishlist.products.count()
        else:
            wishlist_ids = request.session.get('wishlist_ids', [])
            str_id = str(product.id)
            if str_id in wishlist_ids:
                wishlist_ids.remove(str_id)
                message = "Removed from wishlist"
            else:
                wishlist_ids.append(str_id)
                added = True
                message = "Added to wishlist"
            request.session['wishlist_ids'] = wishlist_ids
            request.session.modified = True
            count = len(wishlist_ids)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
            return JsonResponse({
                'success': True,
                'added': added,
                'message': message,
                'wishlist_count': count
            })
        
        messages.success(request, message)
        return redirect(request.META.get('HTTP_REFERER', 'product:product_list'))

class WishlistToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist.products.remove(product)
            wishlist_count = wishlist.products.count()
        else:
            wishlist_ids = request.session.get('wishlist_ids', [])
            str_id = str(product.id)
            if str_id in wishlist_ids:
                wishlist_ids.remove(str_id)
                request.session['wishlist_ids'] = wishlist_ids
                request.session.modified = True
            wishlist_count = len(wishlist_ids)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
            return JsonResponse({
                'success': True,
                'message': f"{product.name} moved to cart",
                'cart_count': cart.items.count(),
                'wishlist_count': wishlist_count
            })
        
        messages.success(request, f"{product.name} moved to cart")
        return redirect('product:wishlist_detail')

class WishlistAddAllToCartView(View):
    def post(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        products = get_wishlist_products(request)
        
        count = 0
        if hasattr(products, 'count'):
             count = products.count()
        else:
             count = len(products)
        
        if count == 0:
            messages.info(request, "Your wishlist is empty.")
            return redirect('product:wishlist_detail')
            
        for product in products:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
                
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist.products.clear()
            wishlist_count = 0
        else:
            request.session['wishlist_ids'] = []
            request.session.modified = True
            wishlist_count = 0
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
            return JsonResponse({
                'success': True,
                'message': f"{count} items moved to cart",
                'cart_count': cart.items.count(),
                'wishlist_count': wishlist_count
            })
            
        messages.success(request, f"{count} items moved to cart")
        return redirect('product:cart_detail')
