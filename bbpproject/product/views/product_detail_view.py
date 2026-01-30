from django.views.generic import DetailView
from ..models import Product

class ProductDetailView(DetailView):
    model = Product
    template_name = "pages/product/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
