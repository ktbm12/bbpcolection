

from django.shortcuts import render, redirect
from django.utils.text import slugify
from product.models import Category


def category_list_create(request):
    categories = Category.objects.all().order_by("name")

    if request.method == "POST":
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

    context = {
        "categories": categories
    }

    return render(
        request,
        "pages/dashboard/include/categori.html",
        context,
    )
