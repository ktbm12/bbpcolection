from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib import messages

from product.models import Product
from product.forms import ProductForm


class ProductDashboardView(FormView):
    template_name = "pages/dashboard/include/create_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("product:dashboard_products")

    # ---------------------------
    # Liste produits optimisée
    # ---------------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["products"] = (
            Product.objects
            .select_related("category")
            .only(
                "id",
                "name",
                "price",
                "old_price",
                "stock",
                "is_featured",
                "main_image",
                "created",
                "category__name",
            )
            .order_by("-created")
        )

        return context

    # ---------------------------
    # Création produit
    # ---------------------------
    def form_valid(self, form):
        product = form.save(commit=False)

        if not product.slug:
            product.slug = slugify(product.name)

        product.save()

        messages.success(self.request, "Produit ajouté avec succès.")
        return super().form_valid(form)


# ---------------------------
# Modification produit
# ---------------------------
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.slug = slugify(obj.name)
            obj.save()
            messages.success(request, "Produit modifié.")
    return redirect("product:dashboard_products")


# ---------------------------
# Suppression produit
# ---------------------------
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Produit supprimé.")
    return redirect("product:dashboard_products")
