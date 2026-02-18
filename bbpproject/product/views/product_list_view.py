# product/views/product_list_view.py
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count
from django.utils.translation import gettext_lazy as _

from ..models import Product, Category


class ProductListView(ListView):
    """
    CBV view that displays the paginated list of products with filters and sorting.
    Supports:
    - Filter by category (via query param ?category=...)
    - Sort by popularity, price, newness, reviews
    - Pagination (12 products per page by default)
    - Simple contextual search (optional)
    """
    model = Product
    template_name = "pages/product/product.html"     # adapte si le template est ailleurs
    context_object_name = "products"
    paginate_by = 12                                # 12 products per page (good mobile/desktop balance)
    ordering = ['-created']                         # default: newest first

    def get_queryset(self):
        """
        Builds the dynamic queryset according to filters and sorting
        """
        qs = Product.objects.filter(is_active=True)

        # 1. Filtre par catégorie (slug)
        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            qs = qs.filter(category=category)

        # 2. Filtre par Prix
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min:
            qs = qs.filter(price__gte=price_min)
        if price_max:
            qs = qs.filter(price__lte=price_max)

        # 3. Filtre Disponibilité
        in_stock = self.request.GET.get('in_stock')
        if in_stock == '1':
            qs = qs.filter(stock__gt=0)

        # 4. Recherche (Nom, Description, Catégorie)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )

        # 5. Dynamic Sorting
        sort = self.request.GET.get('sort')
        if sort:
            if sort == 'price_asc':
                qs = qs.order_by('price')
            elif sort == 'price_desc':
                qs = qs.order_by('-price')
            elif sort == 'newest':
                qs = qs.order_by('-created')
            elif sort == 'rating':
                # Keep option but no real sorting until Review model is integrated
                pass
        
        return qs

    def get_context_data(self, **kwargs):
        """
        Adds useful variables to the template:
        - categories for filters
        - active category
        - active sorting parameter
        """
        context = super().get_context_data(**kwargs)

        # Toutes les catégories actives pour le menu filtre
        context['categories'] = Category.objects.filter(is_active=True).order_by('name')

        # Catégorie actuellement sélectionnée (pour le bouton actif)
        category_slug = self.request.GET.get('category')
        if category_slug:
            context['category'] = get_object_or_404(Category, slug=category_slug)
        else:
            context['category'] = None

        # Tri actif (pour le select)
        context['current_sort'] = self.request.GET.get('sort', '')

        # Nombre total de produits (avant pagination)
        context['total_products'] = self.get_queryset().count()

        return context

    def get_paginate_by(self, queryset):
        """
        Allows overriding the number per page via query param ?page_size=...
        (optional – useful for tests or "see more" mode)
        """
        page_size = self.request.GET.get('page_size')
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.paginate_by