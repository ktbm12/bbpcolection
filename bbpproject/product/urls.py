# product/urls.py
from django.urls import include, path
from .views.product_list_view import ProductListView
from .views.product_detail_view import ProductDetailView
from .views.cart_detail_view import (
    CartDetailView,
    UpdateCartItemView,
    RemoveCartItemView,
    add_to_cart,
    get_cart_count,
    apply_promo_code,
    CheckoutPlaceholderView,
)

from product.views.categorie_view import category_list_create
app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cartdetail/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/count/', get_cart_count, name='cart_count'),
    path('cart/apply-promo/', apply_promo_code, name='apply_promo'),
    path('checkout/', CheckoutPlaceholderView.as_view(), name='checkout'),
    path('update/<uuid:item_id>/', UpdateCartItemView.as_view(), name='update_item'),
    path('remove/<uuid:item_id>/', RemoveCartItemView.as_view(), name='remove_item'),
    path('add/<uuid:product_id>/', add_to_cart, name='add_item'),
    path("categories/", category_list_create, name="category_list"),
]



