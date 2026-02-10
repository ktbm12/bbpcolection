from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from product.models import Product, Review
from product.forms import ReviewForm


@login_required
@require_POST
def submit_review(request, product_id):
    """Handle review submission for a product."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Check if user already reviewed this product
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.error(request, "Vous avez déjà laissé un avis pour ce produit.")
        return redirect('product:product_detail', pk=product_id)
    
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        
        messages.success(request, "Merci pour votre avis ! Il sera visible sous peu.")
        return redirect('product:product_detail', pk=product_id)
    else:
        for error in form.errors.values():
            messages.error(request, error)
        return redirect('product:product_detail', pk=product_id)
