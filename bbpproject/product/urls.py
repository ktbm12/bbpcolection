# product/urls.py
from django.urls import include, path
from .views.product_list_view import ProductListView
from .views.product_detail_view import ProductDetailView
from product.views.categorie_view import category_list_create

from .views.cart_detail_view import (
    CartDetailView,
    UpdateCartItemView,
    RemoveCartItemView,
    add_to_cart,
    get_cart_count,
    apply_promo_code,
    CheckoutPlaceholderView,
)
from .views.produc_create_view import ProductDashboardView
from .views.produc_create_view import product_edit
from .views.produc_create_view import product_delete
from .views.wishlist_view import WishlistView, toggle_wishlist, wishlist_to_cart, wishlist_add_all_to_cart


app_name = "product"

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
    
    # Wishlist
    path('wishlist/', WishlistView.as_view(), name='wishlist_detail'),
    path('wishlist/toggle/<uuid:product_id>/', toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/move-to-cart/<uuid:product_id>/', wishlist_to_cart, name='move_to_cart'),
    path('wishlist/move-all-to-cart/', wishlist_add_all_to_cart, name='wishlist_add_all_to_cart'),
   
    path(
    "dashboard/products/",
    ProductDashboardView.as_view(),
    name="dashboard_products",
),
path("dashboard/products/<uuid:pk>/edit/", product_edit, name="product_edit"),
path("dashboard/products/<uuid:pk>/delete/", product_delete, name="product_delete"),

]



