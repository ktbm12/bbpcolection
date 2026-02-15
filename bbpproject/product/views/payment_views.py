import stripe
import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Cart, Order, OrderItem
from .cart_detail_view import get_or_create_cart, get_cart_summary

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.payment_status == "PAID":
        messages.info(request, "This order is already paid.")
        return redirect('product:order_confirmation')

    # Get cart for metadata
    cart = get_or_create_cart(request)
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Order #{order.order_number}'},
                    'unit_amount': int(order.total_amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('product:payment_success') + f'?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.id}'),
            cancel_url=request.build_absolute_uri(reverse('product:payment_cancel')),
            metadata={
                "order_id": str(order.id),
                "user_id": str(request.user.id),
                "cart_id": str(cart.id) if cart else ""
            }
        )
        return redirect(session.url, code=303)
    except Exception as e:
        messages.error(request, f"Stripe Error: {str(e)}")
        return redirect('product:checkout')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        user_id = session.get('metadata', {}).get('user_id')
        cart_id = session.get('metadata', {}).get('cart_id')
        
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                if order.payment_status != "PAID":
                    order.payment_status = "PAID"
                    order.status = "PROCESSING"
                    order.payment_id = session.id
                    order.payment_method = "STRIPE"
                    order.save()
                    
                    # Clear Cart
                    if cart_id:
                        CartItem.objects.filter(cart_id=cart_id).delete()
                    
                    # Send emails
                    _send_payment_confirmation_emails(order, request)
            except Order.DoesNotExist:
                pass
                
    return HttpResponse(status=200)

def paypal_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE, # "sandbox" or "live"
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('product:payment_success') + f'?order_id={order.id}'),
            "cancel_url": request.build_absolute_uri(reverse('product:checkout'))
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": f"Order #{order.order_number}",
                    "sku": str(order.order_number),
                    "price": str(order.total_amount),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(order.total_amount),
                "currency": "USD"
            },
            "description": "bbpcollection payment"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)
        messages.error(request, "PayPal redirection error.")
    else:
        messages.error(request, f"PayPal Error: {payment.error}")
    return redirect('product:checkout')

class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/payment/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('order_id')
        session_id = self.request.GET.get('session_id')
        
        if order_id:
            order = get_object_or_404(Order, id=order_id, user=self.request.user)
            context['order'] = order
            
            # If Stripe, we might want to double check status if webhook is slow
            if session_id:
                try:
                    session = stripe.checkout.Session.retrieve(session_id)
                    if session.payment_status == 'paid' and order.payment_status != 'PAID':
                        order.payment_status = 'PAID'
                        order.status = 'PROCESSING'
                        order.payment_id = session.id
                        order.payment_method = 'STRIPE'
                        order.save()
                except:
                    pass
        return context

class PaymentCancelView(TemplateView):
    template_name = 'pages/payment/cancel.html'

def _send_payment_confirmation_emails(order, request):
    from core.email_utils import send_templated_email
    from django.contrib.sites.shortcuts import get_current_site
    
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = 'https' if request.is_secure() else 'http'
    
    # User email
    user_context = {
        'user': order.user,
        'order': order,
        'dashboard_url': f"{protocol}://{domain}{reverse('users:user_orders')}"
    }
    send_templated_email(
        subject=f"Payment Confirmed - Order #{order.order_number}",
        to_email=order.user.email,
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
            subject=f"💰 Payment Received: #{order.order_number}",
            to_email=admin_email,
            template_name='emails/admin_new_order.html',
            context=admin_context
        )
