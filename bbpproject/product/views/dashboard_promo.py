from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from ..models import Promotion, PromotionItem, Product
from django.forms import inlineformset_factory

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

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
        messages.success(self.request, "Promotion created successfully.")
        return super().form_valid(form)

class PromotionUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Promotion
    fields = ['name', 'description', 'start_date', 'end_date', 'image', 'is_active']
    template_name = 'pages/dashboard/promo/form.html'
    success_url = reverse_lazy('product:promo_list')

    def form_valid(self, form):
        messages.success(self.request, "Promotion updated.")
        return super().form_valid(form)

class PromotionDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Promotion
    success_url = reverse_lazy('product:promo_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Promotion deleted.")
        return super().delete(request, *args, **kwargs)

class PromotionItemsManageView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, pk):
        promotion = get_object_or_404(Promotion, pk=pk)
        PromotionItemFormSet = inlineformset_factory(
            Promotion, PromotionItem,
            fields=['product', 'promotion_price', 'special_label'],
            extra=3, can_delete=True
        )
        formset = PromotionItemFormSet(instance=promotion)
        return render(request, 'pages/dashboard/promo/items_form.html', {
            'promotion': promotion,
            'formset': formset
        })

    def post(self, request, pk):
        promotion = get_object_or_404(Promotion, pk=pk)
        PromotionItemFormSet = inlineformset_factory(
            Promotion, PromotionItem,
            fields=['product', 'promotion_price', 'special_label'],
            extra=3, can_delete=True
        )
        formset = PromotionItemFormSet(request.POST, instance=promotion)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Promotion items updated.")
            return redirect('product:promo_list')
        
        return render(request, 'pages/dashboard/promo/items_form.html', {
            'promotion': promotion,
            'formset': formset
        })
