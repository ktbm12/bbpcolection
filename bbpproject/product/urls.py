# product/urls.py
from django.urls import path
from .views.product_list_view import ProductListView

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    # path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    # etc.
]