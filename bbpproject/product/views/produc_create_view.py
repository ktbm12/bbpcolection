from django.views.generic import FormView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from product.models import Product
from product.forms import ProductForm, ProductImageFormSet


class ProductDashboardView(LoginRequiredMixin, FormView):
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
        
        image_formset.instance = product
        image_formset.save()

        messages.success(self.request, "Product and gallery added successfully.")
        return redirect(self.success_url)


class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("product:dashboard_products")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.slug = slugify(obj.name)
        obj.save()
        messages.success(self.request, "Product updated.")
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        # Current implementation just redirects to dashboard, possibly showing a modal there?
        # The FBV was just a POST handler that redirects.
        return redirect(self.success_url)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("product:dashboard_products")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Product deleted.")
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # FBV allowed GET delete (which is bad practice but exists in current code)
        return self.delete(request, *args, **kwargs)
