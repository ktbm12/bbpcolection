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


from bbpproject.users.views.dashboards.orders_view import UserOrdersView
from bbpproject.users.views.dashboards.admin_orders_view import (
    AdminOrderListView,
    AdminOrderDetailView,
    update_order_status,
)
from bbpproject.users.views.dashboards.admin_reviews_view import (
    AdminReviewListView,
    toggle_review_approval,
    delete_review,
)

from bbpproject.users.views.static_views import AboutView, ContactView

app_name = "users"

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('dashboard/redirect/', smart_home_redirect_view, name='dashboard_redirect'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/admin/orders/', AdminOrderListView.as_view(), name='admin_orders'),
    path('dashboard/admin/orders/<uuid:pk>/', AdminOrderDetailView.as_view(), name='admin_order_detail'),
    path('dashboard/admin/orders/<uuid:pk>/update-status/', update_order_status, name='update_order_status'),
    path('dashboard/admin/reviews/', AdminReviewListView.as_view(), name='admin_reviews'),
    path('dashboard/admin/reviews/<uuid:pk>/toggle/', toggle_review_approval, name='toggle_review_approval'),
    path('dashboard/admin/reviews/<uuid:pk>/delete/', delete_review, name='delete_review'),
    path('dashboard/user/', UserDashboardView.as_view(), name='user_dashboard'),
    path('dashboard/user/orders/', UserOrdersView.as_view(), name='user_orders'),
]



