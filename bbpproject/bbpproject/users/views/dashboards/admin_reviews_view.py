from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from product.models import Review


@method_decorator(staff_member_required, name='dispatch')
class AdminReviewListView(ListView):
    """Admin view to manage product reviews."""
    model = Review
    template_name = "pages/dashboard/reviews/review_list.html"
    context_object_name = "reviews"
    paginate_by = 20

    def get_queryset(self):
        qs = Review.objects.all().select_related('product', 'user').order_by('-created')
        
        # Filter by approval status
        status = self.request.GET.get('status')
        if status == 'pending':
            qs = qs.filter(is_approved=False)
        elif status == 'approved':
            qs = qs.filter(is_approved=True)
        
        # Filter by rating
        rating = self.request.GET.get('rating')
        if rating:
            qs = qs.filter(rating=rating)
        
        # Search by product name or user
        q = self.request.GET.get('q')
        if q:
            from django.db.models import Q
            qs = qs.filter(
                Q(product__name__icontains=q) |
                Q(user__username__icontains=q) |
                Q(comment__icontains=q)
            )
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        context['current_rating'] = self.request.GET.get('rating', '')
        
        # Stats
        context['total_reviews'] = Review.objects.count()
        context['pending_reviews'] = Review.objects.filter(is_approved=False).count()
        context['approved_reviews'] = Review.objects.filter(is_approved=True).count()
        
        return context


@staff_member_required
@require_POST
def toggle_review_approval(request, pk):
    """Toggle review approval status."""
    review = get_object_or_404(Review, pk=pk)
    review.is_approved = not review.is_approved
    review.save()
    
    status_text = "approuvé" if review.is_approved else "désapprouvé"
    messages.success(request, f"Avis {status_text} avec succès.")
    
    return JsonResponse({
        'success': True,
        'is_approved': review.is_approved,
        'message': f'Avis {status_text}'
    })


@staff_member_required
def delete_review(request, pk):
    """Delete a review."""
    review = get_object_or_404(Review, pk=pk)
    product_name = review.product.name
    review.delete()
    
    messages.success(request, f"Avis supprimé pour {product_name}.")
    return redirect('users:admin_reviews')
