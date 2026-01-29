# bbpproject/users/urls.py

from django.urls import path
from bbpproject.users.views.home_view import home_view     # ← une seule fois bbpproject
app_name = "users"

urlpatterns = [
    path('', home_view, name='home'),
    
]