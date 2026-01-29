from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from core.models import CFPBaseModel
from bbpproject.users.models import User


class Category(CFPBaseModel):
    name = models.CharField(_("nom"), max_length=120, unique=True)
    slug = models.SlugField(_("slug"), unique=True, max_length=140)
    description = models.TextField(blank=True)

    class Meta(CFPBaseModel.Meta):
        verbose_name = _("catégorie")
        verbose_name_plural = _("catégories")

    def __str__(self):
        return self.name

# product/models.py (extrait corrigé)
class Product(CFPBaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="products")
    main_image = models.ImageField(upload_to="products/main/%Y/%m/%d/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(3000)])
    old_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    stock = models.PositiveIntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "produit"
        verbose_name_plural = "produits"
        ordering = ['-is_featured', '-created']          # ← utilise 'created' (TimeStampedModel)
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),  # ← corrigé
        ]

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return round(((self.old_price - self.price) / self.old_price) * 100)
        return 0
class ProductImage(CFPBaseModel):
    """Images secondaires / galerie"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery"
    )
    image = models.ImageField(upload_to="products/gallery/%Y/%m/%d/")
    alt_text = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveSmallIntegerField(default=10)

    class Meta(CFPBaseModel.Meta):
        ordering = ['display_order', 'created']
        verbose_name = _("image secondaire")
        verbose_name_plural = _("images secondaires")


# ────────────────────────────────────────────────
#                  PANIER & COMMANDE
# ────────────────────────────────────────────────


class Cart(CFPBaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts"
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)

    class Meta(CFPBaseModel.Meta):
        verbose_name = _("panier")
        verbose_name_plural = _("paniers")

    @property
    def total_items(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(CFPBaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    class Meta(CFPBaseModel.Meta):
        unique_together = [['cart', 'product']]

    @property
    def subtotal(self):
        return self.quantity * self.product.price


class Order(CFPBaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    total_amount = models.DecimalField(max_digits=12, decimal_places=0)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=30, default="PENDING")  # à remplacer par un choices si besoin
    payment_method = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"CMD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class OrderItem(CFPBaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=0)