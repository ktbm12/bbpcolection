# product/views/product_list_view.py
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count
from django.utils.translation import gettext_lazy as _

from ..models import Product, Category


class ProductListView(ListView):
    """
    Vue CBV qui affiche la liste paginée des produits avec filtres et tri.
    Supporte :
    - Filtre par catégorie (via query param ?category=...)
    - Tri par popularité, prix, nouveautés, avis
    - Pagination (12 produits par page par défaut)
    - Recherche contextuelle simple (optionnel)
    """
    model = Product
    template_name = "product/product_list.html"     # adapte si le template est ailleurs
    context_object_name = "products"
    paginate_by = 12                                # 12 produits par page (bon équilibre mobile/desktop)
    ordering = ['-created']                         # défaut : les plus récents

    def get_queryset(self):
        """
        Construit le queryset dynamique selon les filtres et le tri
        """
        qs = Product.objects.filter(is_active=True)

        # 1. Filtre par catégorie (slug)
        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            qs = qs.filter(category=category)

        # 2. Tri dynamique
        sort = self.request.GET.get('sort')
        if sort:
            if sort == 'price_asc':
                qs = qs.order_by('price')
            elif sort == 'price_desc':
                qs = qs.order_by('-price')
            elif sort == 'newest':
                qs = qs.order_by('-created')
            elif sort == 'rating':
                # Tri par note moyenne + nombre d'avis (plus pondéré)
                qs = qs.annotate(
                    avg_rating=Avg('reviews__rating'),
                    review_count=Count('reviews')
                ).order_by('-avg_rating', '-review_count')

        # Optionnel : recherche texte simple (si tu veux l'ajouter plus tard)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )

        return qs

    def get_context_data(self, **kwargs):
        """
        Ajoute des variables utiles au template :
        - catégories pour les filtres
        - catégorie active
        - paramètre de tri actif
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
        Permet de surcharger le nombre par page via query param ?page_size=...
        (optionnel – utile pour tests ou mode "voir plus")
        """
        page_size = self.request.GET.get('page_size')
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.paginate_by