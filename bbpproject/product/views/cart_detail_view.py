# product/views/cart_detail_view.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, ExpressionWrapper, DecimalField

from ..models import Cart, CartItem, Product

def get_cart_summary(cart):
    """Fonction utilitaire pour renvoyer les données calculées du panier"""
    items = CartItem.objects.filter(cart=cart).aggregate(
        total_items=Sum('quantity'),
        subtotal=Sum(ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField()))
    )

    subtotal = items['subtotal'] or 0
    discount = 0  # Logique promo à ajouter ici si besoin
    free_shipping_threshold = 50000
    shipping_cost = 0 if subtotal >= free_shipping_threshold else 3000
    total = subtotal - discount + shipping_cost

    free_shipping_remaining = max(free_shipping_threshold - subtotal, 0)
    shipping_progress = min(100, (subtotal / free_shipping_threshold) * 100) if free_shipping_threshold else 100

    return {
        'cart_items_count': items['total_items'] or 0,
        'subtotal': float(subtotal),
        'discount': float(discount),
        'shipping_cost': float(shipping_cost),
        'total': float(total),
        'shipping_free': subtotal >= free_shipping_threshold,
        'shipping_progress': round(shipping_progress, 1),
        'shipping_message': (
            "Livraison gratuite appliquée !" if subtotal >= free_shipping_threshold
            else f"Plus que {int(free_shipping_remaining):,} FCFA pour la livraison gratuite"
        ),
    }

def get_or_create_cart(request):
    """
    Récupère le panier actif de l'utilisateur connecté.
    """
    if not request.user.is_authenticated:
        return None

    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart

class CartDetailView(LoginRequiredMixin, TemplateView):
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
class UpdateCartItemView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity < 1: quantity = 1
            item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            item.quantity = quantity
            item.save()
            return JsonResponse({'success': True, **get_cart_summary(item.cart)})
        except (ValueError, CartItem.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalide'}, status=400)

@method_decorator(require_POST, name='dispatch')
class RemoveCartItemView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        try:
            item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            cart = item.cart
            item.delete()
            return JsonResponse({'success': True, **get_cart_summary(cart)})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Introuvable'}, status=404)

@require_POST
@login_required
def add_to_cart(request, product_id):
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
        
        # On doit rafraîchir pour avoir la valeur de F()
        item.refresh_from_db()
        return JsonResponse({'success': True, **get_cart_summary(cart)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def get_cart_count(request):
    cart = get_or_create_cart(request)
    count = CartItem.objects.filter(cart=cart).aggregate(total=Sum('quantity'))['total'] or 0
    return JsonResponse({'count': count})

@require_POST
@login_required
def apply_promo_code(request):
    # Placeholder pour la logique promo
    return JsonResponse({'success': False, 'error': 'Codes promos non activés pour le moment'})

class CheckoutPlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = "pages/product/cart.html"
    
    def get(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.contrib import messages
        messages.info(request, "Le système de paiement sera bientôt disponible.")
        return redirect('product:cart_detail')