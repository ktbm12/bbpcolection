from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import LegalPage
from .forms import LegalPageForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class LegalPageDashboardListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = LegalPage
    template_name = "pages/dashboard/legal/list.html"
    context_object_name = "legal_pages"
    ordering = ["-created"]

class LegalPageDashboardCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = LegalPage
    form_class = LegalPageForm
    template_name = "pages/dashboard/legal/form.html"
    success_url = reverse_lazy("core:dashboard_legal_list")

    def form_valid(self, form):
        messages.success(self.request, "Legal page created successfully.")
        return super().form_valid(form)

class LegalPageDashboardUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = LegalPage
    form_class = LegalPageForm
    template_name = "pages/dashboard/legal/form.html"
    success_url = reverse_lazy("core:dashboard_legal_list")

    def form_valid(self, form):
        messages.success(self.request, "Legal page updated successfully.")
        return super().form_valid(form)

class LegalPageDashboardDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = LegalPage
    success_url = reverse_lazy("core:dashboard_legal_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Legal page deleted successfully.")
        return super().delete(request, *args, **kwargs)


class PrivacyPolicyDashboardUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = LegalPage
    form_class = LegalPageForm
    template_name = "pages/dashboard/legal/form.html"
    success_url = reverse_lazy("core:dashboard_legal_list")

    def get_object(self, queryset=None):
        return get_object_or_404(LegalPage, slug="privacy-policy")

    def form_valid(self, form):
        messages.success(self.request, "Privacy Policy updated successfully.")
        return super().form_valid(form)
