from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.text import slugify
from ..models import Post
from ..forms import PostForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class BlogDashboardListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Post
    template_name = "pages/dashboard/blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 10
    ordering = ['-created']

class PostCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "pages/dashboard/blog/post_form.html"
    success_url = reverse_lazy("blog:dashboard_blog_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "pages/dashboard/blog/post_form.html"
    success_url = reverse_lazy("blog:dashboard_blog_list")

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog:dashboard_blog_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted successfully.")
        return super().delete(request, *args, **kwargs)
