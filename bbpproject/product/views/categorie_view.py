from django.shortcuts import redirect
from django.utils.text import slugify
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import Category


class CategoryListCreateView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "pages/dashboard/include/categori.html"
    context_object_name = "categories"
    ordering = ["name"]

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        description = request.POST.get("description")

        if name:
            slug = slugify(name)
            Category.objects.create(
                name=name,
                slug=slug,
                description=description,
            )
            return redirect("product:category_list")
        
        return self.get(request, *args, **kwargs)
