# bbpproject/users/urls.py

from django.urls import path
from bbpproject.users.views.home_view import home_view
from bbpproject.users.views.dashboards.dashboard_views import (
    AdminDashboardView,
    UserDashboardView,
    smart_home_redirect_view,
)
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from product.models import Product, Category


app_name = "users"

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/redirect/', smart_home_redirect_view, name='dashboard_redirect'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/user/', UserDashboardView.as_view(), name='user_dashboard'),
]



