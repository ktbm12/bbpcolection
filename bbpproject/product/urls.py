# product/urls.py
from django.urls import include, path
from .views.product_list_view import ProductListView
from .views.product_detail_view import ProductDetailView
from product.views.categorie_view import CategoryListCreateView

from .views.cart_detail_view import (
    CartDetailView,
    UpdateCartItemView,
    RemoveCartItemView,
    AddToCartView,
    GetCartCountView,
    ApplyPromoCodeView,
    ClearCartView,
)
from .views.checkout_view import CheckoutView, OrderConfirmationView
from .views.payment_views import (
    StripeCheckoutView,
    StripeWebhookView,
    PaypalCheckoutView,
    PaymentSuccessView,
    PaymentCancelView,
)

from .views.produc_create_view import ProductDashboardView, ProductEditView, ProductDeleteView
from .views.wishlist_view import WishlistView, ToggleWishlistView, WishlistToCartView, WishlistAddAllToCartView
from .views.review_view import SubmitReviewView
from .views.dashboard_promo import (
    PromotionListView, PromotionCreateView, PromotionUpdateView, 
    PromotionDeleteView, PromotionItemsManageView
)

app_name = "product"

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cartdetail/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/count/', GetCartCountView.as_view(), name='cart_count'),
    path('cart/apply-promo/', ApplyPromoCodeView.as_view(), name='apply_promo'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/confirmation/', OrderConfirmationView.as_view(), name='order_confirmation'),
    path('update/<uuid:item_id>/', UpdateCartItemView.as_view(), name='update_item'),
    path('remove/<uuid:item_id>/', RemoveCartItemView.as_view(), name='remove_item'),
    path('add/<uuid:product_id>/', AddToCartView.as_view(), name='add_item'),
    path("categories/", CategoryListCreateView.as_view(), name="category_list"),
    
    # Wishlist
    path('wishlist/', WishlistView.as_view(), name='wishlist_detail'),
    path('wishlist/toggle/<uuid:product_id>/', ToggleWishlistView.as_view(), name='toggle_wishlist'),
    path('wishlist/move-to-cart/<uuid:product_id>/', WishlistToCartView.as_view(), name='move_to_cart'),
    path('wishlist/move-all-to-cart/', WishlistAddAllToCartView.as_view(), name='wishlist_add_all_to_cart'),
    
    # Reviews
    path('<uuid:product_id>/review/submit/', SubmitReviewView.as_view(), name='submit_review'),
   
    path(
    "dashboard/products/",
    ProductDashboardView.as_view(),
    name="dashboard_products",
),
path("dashboard/products/<uuid:pk>/edit/", ProductEditView.as_view(), name="product_edit"),
path("dashboard/products/<uuid:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    
    # Promotions Dashboard
    path('dashboard/promotions/', PromotionListView.as_view(), name='promo_list'),
    path('dashboard/promotions/add/', PromotionCreateView.as_view(), name='promo_create'),
    path('dashboard/promotions/<uuid:pk>/edit/', PromotionUpdateView.as_view(), name='promo_edit'),
    path('dashboard/promotions/<uuid:pk>/delete/', PromotionDeleteView.as_view(), name='promo_delete'),
    path('dashboard/promotions/<uuid:pk>/items/', PromotionItemsManageView.as_view(), name='promo_items_manage'),

    # Payments
    path('payment/stripe/<uuid:order_id>/', StripeCheckoutView.as_view(), name='stripe_checkout'),
    path('payment/stripe/webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),
    path('payment/paypal/<uuid:order_id>/', PaypalCheckoutView.as_view(), name='paypal_checkout'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/cancel/', PaymentCancelView.as_view(), name='payment_cancel'),

]
