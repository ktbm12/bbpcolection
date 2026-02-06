class ProductListView(ListView):
    model = Product
    template_name = "pages/dashboard/include/product_list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        return (
            Product.objects
            .select_related("category")  # évite requêtes N+1
            .only(
                "id",
                "name",
                "slug",
                "price",
                "old_price",
                "stock",
                "is_featured",
                "created",
                "category__name",
            )
            .order_by("-is_featured", "-created")
        )
class ProductCreateView(CreateView):
    model = Product
    template_name = "pages/dashboard/include/create_product.html"
    fields = [
        "name",
        "category",
        "main_image",
        "price",
        "old_price",
        "stock",
        "is_featured",
        "description",
    ]

    success_url = reverse_lazy("product:product_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.slug = slugify(obj.name)
        obj.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Product.objects.select_related("category")


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "pages/dashboard/include/create_product.html"
    fields = [
        "name",
        "category",
        "main_image",
        "price",
        "old_price",
        "stock",
        "is_featured",
        "description",
    ]

    success_url = reverse_lazy("product:product_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.slug = slugify(obj.name)
        obj.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Product.objects.select_related("category")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("product:product_list")
    template_name = "pages/dashboard/include/product_confirm_delete.html"

    def get_queryset(self):
        return Product.objects.only("id", "name")
