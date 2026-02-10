from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from product.models import Order

class UserOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "pages/user_dashboard/orders.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created').prefetch_related('items', 'items__product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add sidebar context data if needed (user, loyalty points usually via context processors or duplicate logic)
        # For now, base_user.html might need some of this. 
        # But base_user.html usually expects 'user' which is always there.
        # UserDashboardView adds 'loyalty_points', 'pending_orders_count' etc.
        # We should probably duplicate some of that logic or create a mixin.
        
        user = self.request.user
        context['pending_orders_count'] = Order.objects.filter(user=user, status__iexact='PENDING').count()
        context['loyalty_points'] = getattr(user, 'loyalty_points', 0)
        return context
