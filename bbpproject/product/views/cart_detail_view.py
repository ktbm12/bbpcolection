# product/views/cart_detail_view.py
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum, ExpressionWrapper, DecimalField

from decimal import Decimal

from ..models import Cart, CartItem, Product

def get_cart_summary(cart):
    """Utility function to return calculated cart data in USD."""
    items = CartItem.objects.filter(cart=cart).aggregate(
        total_items=Sum('quantity'),
        subtotal=Sum(ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField()))
    )

    subtotal = items['subtotal'] or Decimal('0.00')
    discount = Decimal('0.00')  # Promo logic to be added
    free_shipping_threshold = Decimal('100.00')
    shipping_cost = Decimal('0.00') if subtotal >= free_shipping_threshold else Decimal('9.99')
    total = subtotal - discount + shipping_cost

    free_shipping_remaining = max(free_shipping_threshold - subtotal, Decimal('0.00'))
    shipping_progress = min(100, float((subtotal / free_shipping_threshold) * 100)) if free_shipping_threshold else 100

    return {
        'cart_items_count': items['total_items'] or 0,
        'subtotal': subtotal,
        'discount': discount,
        'shipping_cost': shipping_cost,
        'total': total,
        'shipping_free': subtotal >= free_shipping_threshold,
        'shipping_progress': round(shipping_progress, 1),
        'shipping_message': (
            "Free shipping applied!" if subtotal >= free_shipping_threshold
            else f"Only ${float(free_shipping_remaining):.2f} away from free shipping"
        ),
    }

def get_or_create_cart(request):
    """
    Retrieves the active cart for the user (authenticated or guest via session).
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart

    if not request.session.session_key:
        request.session.create()
    
    cart_id = request.session.get('cart_id')
    cart = None
    
    if cart_id:
        cart = Cart.objects.filter(id=cart_id, user__isnull=True).first()
        
    if not cart:
        cart = Cart.objects.create(session_key=request.session.session_key, user=None)
        request.session['cart_id'] = str(cart.id)
        request.session.modified = True
        
    return cart

class CartDetailView(TemplateView):
    template_name = "pages/product/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)

        cart_items = CartItem.objects.filter(cart=cart).select_related(
            'product', 'product__category'
        ).annotate(
            line_total=ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField()
            )
        )

        summary = get_cart_summary(cart)
        
        context.update(summary)
        context.update({
            'cart': cart,
            'cart_items': cart_items,
            'recommended_products': Product.objects.filter(is_active=True, is_featured=True)[:4],
        })
        return context

@method_decorator(require_POST, name='dispatch')
class UpdateCartItemView(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        try:
            import json
            data = json.loads(request.body)
            quantity = data.get('quantity')
        except:
            quantity = request.POST.get('quantity')
            
        try:
            quantity = int(quantity)
            if quantity < 1: quantity = 1
            
            current_cart = get_or_create_cart(request)
            item = get_object_or_404(CartItem, id=item_id, cart=current_cart)
            
            item.quantity = quantity
            item.save()
            return JsonResponse({'success': True, **get_cart_summary(item.cart)})
        except (ValueError, CartItem.DoesNotExist, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid quantity'}, status=400)

@method_decorator(require_POST, name='dispatch')
class RemoveCartItemView(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        try:
            current_cart = get_or_create_cart(request)
            item = get_object_or_404(CartItem, id=item_id, cart=current_cart)
            
            cart = item.cart
            item.delete()
            return JsonResponse({'success': True, **get_cart_summary(cart)})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)

@method_decorator(require_POST, name='dispatch')
class ClearCartView(View):
    def post(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        return JsonResponse({'success': True, **get_cart_summary(cart)})

@method_decorator(require_POST, name='dispatch')
class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        try:
            product = get_object_or_404(Product, id=product_id, is_active=True)
            quantity = int(request.POST.get('quantity', 1))
            cart = get_or_create_cart(request)
            item, created = CartItem.objects.get_or_create(
                cart=cart, product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                item.quantity = F('quantity') + quantity
                item.save(update_fields=['quantity'])
            
            item.refresh_from_db()
            return JsonResponse({'success': True, **get_cart_summary(cart)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

class GetCartCountView(View):
    def get(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        count = CartItem.objects.filter(cart=cart).aggregate(total=Sum('quantity'))['total'] or 0
        return JsonResponse({'count': count})

@method_decorator(require_POST, name='dispatch')
class ApplyPromoCodeView(View):
    def post(self, request, *args, **kwargs):
        # Placeholder for promo logic
        return JsonResponse({'success': False, 'error': 'Promo codes are not active yet'})

class CheckoutPlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = "pages/product/cart.html"
    
    def get(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.contrib import messages
        messages.info(request, "The payment system will be available soon.")
        return redirect('product:cart_detail')