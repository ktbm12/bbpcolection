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
            messages.warning(request, "Your cart is empty.")
            return redirect("product:cart_detail")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        cart = get_or_create_cart(self.request)
        if not cart or cart.items.count() == 0:
             messages.error(self.request, "Empty cart.")
             return redirect("product:cart_detail")

        try:
            with transaction.atomic():
                summary = get_cart_summary(cart)
                payment_method = form.cleaned_data['payment_method']
                
                # Create Order
                order = Order.objects.create(
                    user=self.request.user,
                    total_amount=summary['total'],
                    shipping_address=form.cleaned_data['shipping_address'],
                    shipping_city=form.cleaned_data['shipping_city'],
                    shipping_phone=form.cleaned_data['shipping_phone'],
                    status="PENDING",
                    payment_method=payment_method,
                    payment_status="PENDING"
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
                
                # We don't clear the cart or send emails here for Stripe/PayPal
                # because we wait for verification. 
                # For Cash, we do it now.
                
                if payment_method == 'CASH':
                    # Clear Cart
                    cart_items.delete()
                    # Save order ID in session
                    self.request.session['last_order_id'] = str(order.id)
                    
                    # Send Emails
                    self._send_order_emails(order)
                    return super().form_valid(form)
                
                elif payment_method == 'STRIPE':
                    return redirect('product:stripe_checkout', order_id=order.id)
                
                elif payment_method == 'PAYPAL':
                    return redirect('product:paypal_checkout', order_id=order.id)

        except Exception as e:
            messages.error(self.request, f"Error during order: {str(e)}")
            return self.form_invalid(form)
            
        return super().form_valid(form)

    def _send_order_emails(self, order):
        from core.email_utils import send_templated_email
        from django.contrib.sites.shortcuts import get_current_site
        from django.conf import settings
        
        current_site = get_current_site(self.request)
        domain = current_site.domain
        protocol = 'https' if self.request.is_secure() else 'http'
        
        # User email
        user_context = {
            'user': self.request.user,
            'order': order,
            'dashboard_url': f"{protocol}://{domain}{reverse('users:user_orders')}"
        }
        send_templated_email(
            subject=f"Order Confirmation #{order.order_number} - bbpcollection",
            to_email=self.request.user.email,
            template_name='emails/order_confirmation.html',
            context=user_context
        )
        
        # Admin email
        admin_context = {
            'order': order,
            'admin_url': f"{protocol}://{domain}{reverse('users:admin_order_detail', kwargs={'pk': order.pk})}"
        }
        if hasattr(settings, 'ADMINS') and settings.ADMINS:
            admin_email = settings.ADMINS[0][1]
            send_templated_email(
                subject=f"🔔 New order: #{order.order_number}",
                to_email=admin_email,
                template_name='emails/admin_new_order.html',
                context=admin_context
            )

class OrderConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = "pages/product/order_confirmation.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('last_order_id')
        if order_id:
            context['order'] = get_object_or_404(Order, id=order_id, user=self.request.user)
        return context
