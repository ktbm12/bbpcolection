from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import LegalPage

class LegalPageView(DetailView):
    model = LegalPage
    template_name = "pages/legal/legal_page.html"
    context_object_name = "legal_page"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return LegalPage.objects.filter(is_active=True)
