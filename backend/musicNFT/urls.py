import logging

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend.dashboard.views import OrderView

logger = logging.getLogger(__name__)

# logger.info(f"DEBUG: {settings.DEBUG}")

urlpatterns = [
    # Django Admin, use
    path("admin/", admin.site.urls),
    # Home page
    path("", TemplateView.as_view(template_name="home.html")),
    # User management
    path("api/user/", include("backend.users.urls", namespace="users")),
    #  JWT token generation paths
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/order/", OrderView.as_view(), name="order"),
    path("api/dashboard/", include("backend.dashboard.urls", namespace="dashboard")),
]

# if settings.DEBUG:
urlpatterns += staticfiles_urlpatterns()
