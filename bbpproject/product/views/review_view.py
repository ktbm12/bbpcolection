from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from product.models import Product, Review
from product.forms import ReviewForm


class SubmitReviewView(LoginRequiredMixin, View):
    """Handle review submission for a product."""

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Check if user already reviewed this product
        existing_review = Review.objects.filter(product=product, user=request.user).first()
        if existing_review:
            messages.error(request, "You have already left a review for this product.")
            return redirect('product:product_detail', pk=product_id)
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            
            messages.success(request, "Thank you for your review! It will be visible shortly.")
            return redirect('product:product_detail', pk=product_id)
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('product:product_detail', pk=product_id)
