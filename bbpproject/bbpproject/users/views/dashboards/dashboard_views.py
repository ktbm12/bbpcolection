from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dashboard/admin_dashboards.html"

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dashboard/user_dashboard.html"

@login_required
def smart_home_redirect_view(request):
    """
    Redirects the user to the appropriate dashboard based on their status.
    """
    if request.user.is_staff or request.user.is_superuser:
        return redirect("users:admin_dashboard")
    return redirect("users:user_dashboard")
