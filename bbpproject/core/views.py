from django.views.generic import DetailView, TemplateView
from django.shortcuts import get_object_or_404
from .models import LegalPage, PrivacyPolicy

class LegalPageView(DetailView):
    model = LegalPage
    template_name = "pages/legal/legal_page.html"
    context_object_name = "legal_page"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return LegalPage.objects.filter(is_active=True)


class PrivacyPolicyView(TemplateView):
    template_name = "pages/legal/legal_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legal_page'] = PrivacyPolicy.load()
        return context
