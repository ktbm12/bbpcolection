from django.views.generic import DetailView
from ..models import Product

class ProductDetailView(DetailView):
    model = Product
    template_name = "pages/product/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recommandations : produits de la même catégorie, excluant le produit actuel
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context
