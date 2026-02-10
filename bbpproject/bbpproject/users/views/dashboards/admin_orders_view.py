from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from product.models import Order, OrderItem


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderListView(ListView):
    """List all orders for admin with filtering."""
    model = Order
    template_name = "pages/dashboard/orders/order_list.html"
    context_object_name = "orders"
    paginate_by = 20

    def get_queryset(self):
        qs = Order.objects.all().select_related('user').prefetch_related('items').order_by('-created')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status__iexact=status)
        
        # Search by order number or user name
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                models.Q(order_number__icontains=q) |
                models.Q(user__username__icontains=q) |
                models.Q(user__email__icontains=q)
            )
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        
        # Order stats
        from django.db.models import Count, Sum
        context['total_orders'] = Order.objects.count()
        context['pending_orders'] = Order.objects.filter(status='PENDING').count()
        context['total_revenue'] = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        
        return context


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderDetailView(DetailView):
    """View order details and allow status updates."""
    model = Order
    template_name = "pages/dashboard/orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.select_related('user').prefetch_related('items__product')


@staff_member_required
@require_POST
def update_order_status(request, pk):
    """AJAX endpoint to update order status."""
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    
    valid_statuses = ['PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED']
    
    if new_status in valid_statuses:
        order.status = new_status
        order.save()
        
        messages.success(request, f"Commande #{order.order_number} mise à jour vers '{new_status}'.")
        
        return JsonResponse({
            'success': True,
            'status': new_status,
            'message': f'Statut mis à jour: {new_status}'
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Statut invalide'
    }, status=400)
