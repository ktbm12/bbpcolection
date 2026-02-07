from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib import messages

from product.models import Product
from product.forms import ProductForm, ProductImageFormSet


class ProductDashboardView(FormView):
    template_name = "pages/dashboard/include/create_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("product:dashboard_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ProductImageFormSet()
        
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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        image_formset = ProductImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and image_formset.is_valid():
            return self.form_valid(form, image_formset)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, image_formset):
        product = form.save(commit=False)
        if not product.slug:
            product.slug = slugify(product.name)
        product.save()
        
        # Sauvegarde des images de la galerie
        image_formset.instance = product
        image_formset.save()

        messages.success(self.request, "Produit et galerie ajoutés avec succès.")
        return redirect(self.success_url)


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
