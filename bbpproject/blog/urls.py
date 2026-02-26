from django.urls import path
from .views.dashboard_views import (
    BlogDashboardListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

app_name = "blog"

urlpatterns = [
    # Dashboard views
    path('dashboard/', BlogDashboardListView.as_view(), name='dashboard_blog_list'),
    path('dashboard/create/', PostCreateView.as_view(), name='post_create'),
    path('dashboard/<uuid:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('dashboard/<uuid:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
