from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from ..models import Order, OrderItem, Cart, CartItem
from ..forms import ShippingForm
from .cart_detail_view import get_or_create_cart, get_cart_summary

@method_decorator(never_cache, name='dispatch')
class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "pages/product/checkout.html"
    form_class = ShippingForm
    success_url = reverse_lazy("product:order_confirmation")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        if not cart:
            return context
            
        summary = get_cart_summary(cart)
        context.update(summary)
        context['cart_items'] = cart.items.select_related('product').all()
        return context

    def get(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        if not cart or cart.items.count() == 0:
            messages.warning(request, "Votre panier est vide.")
            return redirect("product:cart_detail")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        cart = get_or_create_cart(self.request)
        if not cart or cart.items.count() == 0:
             messages.error(self.request, "Panier vide.")
             return redirect("product:cart_detail")

        try:
            with transaction.atomic():
                summary = get_cart_summary(cart)
                
                # Create Order
                order = Order.objects.create(
                    user=self.request.user,
                    total_amount=summary['total'],
                    shipping_address=form.cleaned_data['shipping_address'],
                    shipping_city=form.cleaned_data['shipping_city'],
                    shipping_phone=form.cleaned_data['shipping_phone'],
                    status="PENDING",
                    payment_method="CASH" # Simplified
                )
                
                # Create Order Items
                cart_items = cart.items.select_related('product').all()
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        unit_price=item.product.price,
                        subtotal=item.subtotal
                    )
                    
                # Clear Cart
                cart_items.delete()
                # Or cart.delete() if you want to reset session cart? No, just clear items.
                
                # Save order ID in session
                self.request.session['last_order_id'] = str(order.id)
                
        except Exception as e:
            messages.error(self.request, f"Erreur lors de la commande: {str(e)}")
            return self.form_invalid(form)
            
        return super().form_valid(form)

class OrderConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = "pages/product/order_confirmation.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('last_order_id')
        if order_id:
            context['order'] = get_object_or_404(Order, id=order_id, user=self.request.user)
        return context
