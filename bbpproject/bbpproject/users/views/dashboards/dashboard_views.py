from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.db.models import Sum
from product.models import Order, Wishlist

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dashboard/admin_dashboards.html"

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "pages/user_dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Commandes
        orders = Order.objects.filter(user=user).order_by('-created')
        context['order_count'] = orders.count()
        context['total_spent'] = orders.aggregate(total=Sum('total_amount'))['total'] or 0
        context['pending_orders_count'] = orders.filter(status__iexact='PENDING').count()
        context['recent_orders'] = orders[:3]
        
        # Liste de souhaits
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        context['wishlist_count'] = wishlist.products.count()
        context['wishlist_preview'] = wishlist.products.all()[:4]
        
        # Fidélité et Parrainage (Champs ajoutés au modèle User)
        context['loyalty_points'] = user.loyalty_points
        context['referral_code'] = user.referral_code or f"{user.username.upper()}2026"
        
        # Simulation d'autres données si nécessaire
        context['referral_count'] = 0 # À implémenter si un modèle Referral existe
        context['referral_earnings'] = 0
        
        return context

@login_required
def smart_home_redirect_view(request):
    """
    Redirects the user to the appropriate dashboard based on their status.
    """
    if request.user.is_staff or request.user.is_superuser:
        return redirect("users:admin_dashboard")
    return redirect("users:user_dashboard")
