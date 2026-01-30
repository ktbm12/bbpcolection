from django.contrib import admin

# Register your models here.
# product/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    Category, Product, ProductImage,
    Cart, CartItem, Order, OrderItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created', 'modified')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created', 'modified')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'display_order', 'is_main')
    readonly_fields = ('created',)
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "is_featured", "category")
    list_filter = ("category", "is_featured", "is_active")  # uniquement de vrais champs
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("old_price",)
    def price_display(self, obj):
        if obj.old_price and obj.old_price > obj.price:
            return format_html(
                '{} <s class="text-gray-400">{}</s>',
                f"{obj.price:,} FCFA",
                f"{obj.old_price:,} FCFA"
            )
        return f"{obj.price:,} FCFA"
    price_display.short_description = _("Prix")

    def discount_percentage(self, obj):
        return f"{obj.discount_percentage}%"
    discount_percentage.short_description = _("Promo")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'display_order', 'created')
    list_filter = ('product__category',)
    search_fields = ('product__name', 'alt_text')
    readonly_fields = ('created',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = _("Aperçu")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'created', 'modified')
    list_filter = ('created',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created', 'modified')
    fields = ('user', 'session_key', 'created', 'modified')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "subtotal")  # remplacer line_total par subtotal
    readonly_fields = ("subtotal",)  # added_at n'existe pas, donc on ne peut pas le mettre
    list_filter = ("cart", "product")

admin.site.register(CartItem, CartItemAdmin)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'user', 'status', 'total_amount',
        'created', 'modified'
    )
    list_filter = ('status', 'created', 'modified')
    search_fields = ('order_number', 'user__username', 'user__email')
    readonly_fields = ('order_number', 'created', 'modified')
    date_hierarchy = 'created'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('order__status', 'product__category')
    search_fields = ('product__name', 'order__order_number')
    readonly_fields = ('subtotal',)