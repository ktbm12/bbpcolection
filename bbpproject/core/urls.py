from django.urls import path
from .views import LegalPageView, PrivacyPolicyView
from .views_dashboard_legal import (
    LegalPageDashboardListView,
    LegalPageDashboardCreateView,
    LegalPageDashboardUpdateView,
    LegalPageDashboardDeleteView,
    PrivacyPolicyDashboardUpdateView
)

app_name = "core"

urlpatterns = [
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy_policy"),
    path("legal/<slug:slug>/", LegalPageView.as_view(), name="legal_page_detail"),
    path("dashboard/admin/legal/", LegalPageDashboardListView.as_view(), name="dashboard_legal_list"),
    path("dashboard/admin/privacy-policy/", PrivacyPolicyDashboardUpdateView.as_view(), name="dashboard_privacy_policy_update"),
    path("dashboard/admin/legal/create/", LegalPageDashboardCreateView.as_view(), name="dashboard_legal_create"),
    path("dashboard/admin/legal/<uuid:pk>/update/", LegalPageDashboardUpdateView.as_view(), name="dashboard_legal_update"),
    path("dashboard/admin/legal/<uuid:pk>/delete/", LegalPageDashboardDeleteView.as_view(), name="dashboard_legal_delete"),
]
