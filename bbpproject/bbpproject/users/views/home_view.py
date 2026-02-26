from django.shortcuts import render
from product.models import Product, Category
from blog.models import Post

def home_view(request):
    context = {
        'categories': Category.objects.filter(is_active=True),
        'featured_products': Product.objects.filter(is_active=True, is_featured=True)[:8],
        'new_arrivals': Product.objects.filter(is_active=True).order_by('-created')[:8],
        'blog_posts': Post.objects.filter(is_published=True).order_by('-created')[:3],
    }
    return render(request, 'pages/home.html', context)
