# product/views/cart_detail_view.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, ExpressionWrapper, DecimalField

from ..models import Cart, CartItem, Product

# product/views/cart_detail_view.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
# ... autres imports ...

def get_or_create_cart(request):
    """
    Récupère le panier actif de l'utilisateur connecté ou en crée un nouveau.
    """
    if not request.user.is_authenticated:
        # Pour les tests ou si tu veux gérer les sessions anonymes plus tard
        return None

    cart, created = Cart.objects.get_or_create(
        user=request.user,
        defaults={'session_key': request.session.session_key if not request.user.is_authenticated else None}
    )
    return cart
class CartDetailView(LoginRequiredMixin, TemplateView):
    """
    Vue principale du panier (affichage + contexte)
    """
    template_name = "cart/cart_detail.html"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupère ou crée le panier de l'utilisateur
        cart = get_or_create_cart(self.request)

        # Items du panier avec annotations utiles
        cart_items = CartItem.objects.filter(cart=cart).select_related(
            'product', 'product__category'
        ).annotate(
            line_total=ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField()
            )
        )

        # Calculs globaux
        subtotal = cart_items.aggregate(
            total=Sum('line_total')
        )['total'] or 0

        # Exemple de promo (à adapter selon ta logique)
        discount = 0  # ou appelle une fonction get_active_discount(cart)
        shipping_cost = 0 if subtotal >= 50000 else 3000  # exemple seuil 50 000 FCFA
        total = subtotal - discount + shipping_cost

        free_shipping_threshold = 50000
        free_shipping_remaining = max(free_shipping_threshold - subtotal, 0)
        shipping_progress = min(100, (subtotal / free_shipping_threshold) * 100) if free_shipping_threshold else 100

        context.update({
            'cart': cart,
            'cart_items': cart_items,
            'cart_items_count': cart_items.count(),
            'subtotal': subtotal,
            'discount': discount,
            'shipping_cost': shipping_cost,
            'total': total,
            'free_shipping_threshold': free_shipping_threshold,
            'free_shipping_remaining': free_shipping_remaining,
            'shipping_progress': round(shipping_progress, 1),
            'recommended_products': Product.objects.filter(is_active=True, is_featured=True)[:4],
        })

        return context


# ────────────────────────────────────────────────
#         Endpoints AJAX (mises à jour panier)
# ────────────────────────────────────────────────


@method_decorator(require_POST, name='dispatch')
class UpdateCartItemView(LoginRequiredMixin, TemplateView):
    """
    AJAX - Mise à jour quantité d'un item
    """
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        quantity = request.POST.get('quantity')

        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1

            item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            item.quantity = quantity
            item.save()

            # Recalcul global
            cart = item.cart
            data = self._get_cart_summary(cart)

            return JsonResponse({'success': True, **data})

        except (ValueError, CartItem.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Quantité invalide ou article introuvable'}, status=400)


@method_decorator(require_POST, name='dispatch')
class RemoveCartItemView(LoginRequiredMixin, TemplateView):
    """
    AJAX - Suppression d'un item
    """
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')

        try:
            item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            cart = item.cart
            item.delete()

            data = self._get_cart_summary(cart)
            return JsonResponse({'success': True, **data})

        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Article introuvable'}, status=404)


def _get_cart_summary(self, cart):
    """Méthode helper pour renvoyer les données mises à jour"""
    items = CartItem.objects.filter(cart=cart).aggregate(
        total_items=Sum('quantity'),
        subtotal=Sum(ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField()))
    )

    subtotal = items['subtotal'] or 0
    discount = 0  # ← à implémenter selon ta logique promo
    shipping_cost = 0 if subtotal >= 50000 else 3000
    total = subtotal - discount + shipping_cost

    free_shipping_threshold = 50000
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


# Bonus : endpoint pour ajouter au panier (depuis les pages produits)
@require_POST
@login_required
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))

        cart = get_or_create_cart(request)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            item.quantity = F('quantity') + quantity
            item.save(update_fields=['quantity'])

        data = CartDetailView()._get_cart_summary(cart)  # réutilise la logique
        return JsonResponse({'success': True, **data})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)