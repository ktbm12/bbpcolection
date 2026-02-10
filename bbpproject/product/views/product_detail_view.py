from django.views.generic import DetailView
from ..models import Product, Review
from product.forms import ReviewForm

class ProductDetailView(DetailView):
    model = Product
    template_name = "pages/product/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Related products
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        
        # Reviews
        context['reviews'] = self.object.reviews.filter(is_approved=True).select_related('user').order_by('-created')[:10]
        context['review_form'] = ReviewForm()
        
        # Check if user has already reviewed
        if self.request.user.is_authenticated:
            context['user_has_reviewed'] = Review.objects.filter(
                product=self.object,
                user=self.request.user
            ).exists()
        else:
            context['user_has_reviewed'] = False
            
        return context
