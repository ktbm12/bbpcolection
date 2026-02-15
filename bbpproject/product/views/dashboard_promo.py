from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from ..models import Promotion, PromotionItem, Product
from django.forms import inlineformset_factory

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class PromotionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Promotion
    template_name = 'pages/dashboard/promo/list.html'
    context_object_name = 'promotions'

class PromotionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Promotion
    fields = ['name', 'description', 'start_date', 'end_date', 'image', 'is_active']
    template_name = 'pages/dashboard/promo/form.html'
    success_url = reverse_lazy('product:promo_list')

    def form_valid(self, form):
        messages.success(self.request, "Promotion créée avec succès.")
        return super().form_valid(form)

class PromotionUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Promotion
    fields = ['name', 'description', 'start_date', 'end_date', 'image', 'is_active']
    template_name = 'pages/dashboard/promo/form.html'
    success_url = reverse_lazy('product:promo_list')

    def form_valid(self, form):
        messages.success(self.request, "Promotion mise à jour.")
        return super().form_valid(form)

class PromotionDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Promotion
    success_url = reverse_lazy('product:promo_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Promotion supprimée.")
        return super().delete(request, *args, **kwargs)

# Promotion Items Management
def promo_items_manage(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    PromotionItemFormSet = inlineformset_factory(
        Promotion, PromotionItem,
        fields=['product', 'promotion_price', 'special_label'],
        extra=3, can_delete=True
    )

    if request.method == 'POST':
        formset = PromotionItemFormSet(request.POST, instance=promotion)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Produits de la promotion mis à jour.")
            return redirect('product:promo_list')
    else:
        formset = PromotionItemFormSet(instance=promotion)
    
    return render(request, 'pages/dashboard/promo/items_form.html', {
        'promotion': promotion,
        'formset': formset
    })
