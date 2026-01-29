# product/urls.py
from django.urls import include, path
from .views.product_list_view import ProductListView
from .views.cart_detail_view import (
    CartDetailView,
    UpdateCartItemView,
    RemoveCartItemView,
    add_to_cart,
)


app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
     path('cartdetail/', CartDetailView.as_view(), name='cart_detail'),
    path('update/<int:item_id>/', UpdateCartItemView.as_view(), name='update_item'),
    path('remove/<int:item_id>/', RemoveCartItemView.as_view(), name='remove_item'),
    path('add/<int:product_id>/', add_to_cart, name='add_item'),
    
    # etc.
]

