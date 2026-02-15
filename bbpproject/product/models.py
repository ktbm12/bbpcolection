from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from core.models import CFPBaseModel
from bbpproject.users.models import User
import uuid


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

    @property
    def avg_rating(self):
        """Calculate average rating from approved reviews."""
        from django.db.models import Avg
        result = self.reviews.filter(is_approved=True).aggregate(avg=Avg('rating'))
        return round(result['avg'], 1) if result['avg'] else 0

    @property
    def review_count(self):
        """Count approved reviews."""
        return self.reviews.filter(is_approved=True).count()

    @property
    def get_main_image_url(self):
        """Retourne l'image principale ou la première image de la galerie comme fallback."""
        if self.main_image:
            return self.main_image.url
        first_img = self.gallery.filter(is_main=True).first() or self.gallery.first()
        if first_img:
            return first_img.image.url
        return None
class ProductImage(CFPBaseModel):
    """Images secondaires / galerie"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery"
    )
    image = models.ImageField(upload_to="products/gallery/%Y/%m/%d/")
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
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
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]
    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="PENDING")
    payment_method = models.CharField(max_length=50, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
    payment_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"CMD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def number(self):
        return self.order_number

    @property
    def total(self):
        return self.total_amount

    @property
    def first_item(self):
        return self.items.first()

    @property
    def first_item_name(self):
        item = self.first_item
        return item.product.name if item else "Aucun article"

    @property
    def first_item_image(self):
        item = self.first_item
        if item and item.product.main_image:
            return item.product.main_image
        return None

    @property
    def items_count(self):
        return self.items.count()


class OrderItem(CFPBaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=0)


class Wishlist(CFPBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField(Product, related_name="wishlisted_by")

    class Meta(CFPBaseModel.Meta):
        verbose_name = _("liste de souhaits")
        verbose_name_plural = _("listes de souhaits")

    def __str__(self):
        return f"Wishlist de {self.user.username}"


class Review(CFPBaseModel):
    """Customer reviews for products."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)  # Admin moderation
    
    class Meta(CFPBaseModel.Meta):
        verbose_name = _("avis")
        verbose_name_plural = _("avis")
        unique_together = ['product', 'user']  # One review per user per product
        ordering = ['-created']

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name} ({self.rating}★)"

    def save(self, *args, **kwargs):
        # Check if user has purchased this product
        if not self.pk:  # Only on creation
            has_purchased = OrderItem.objects.filter(
                order__user=self.user,
                product=self.product,
                order__status__in=['DELIVERED', 'CONFIRMED']
            ).exists()
            self.is_verified_purchase = has_purchased
        super().save(*args, **kwargs)


class Promotion(CFPBaseModel):
    name = models.CharField(_("promotion name"), max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to="promotions/%Y/%m/%d/", blank=True, null=True)
    
    class Meta(CFPBaseModel.Meta):
        verbose_name = _("promotion")
        verbose_name_plural = _("promotions")

    def __str__(self):
        return self.name

    @property
    def is_currently_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date


class PromotionItem(CFPBaseModel):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="promotion_items")
    promotion_price = models.DecimalField(max_digits=10, decimal_places=0)
    special_label = models.CharField(max_length=50, blank=True, help_text="Ex: Flash Sale, -50%, etc.")

    class Meta(CFPBaseModel.Meta):
        verbose_name = _("promotion item")
        verbose_name_plural = _("promotion items")
        unique_together = ['promotion', 'product']

    def __str__(self):
        return f"{self.product.name} in {self.promotion.name}"