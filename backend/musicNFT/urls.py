import logging

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend.users.views import TestView

logger = logging.getLogger(__name__)

# logger.info(f"DEBUG: {settings.DEBUG}")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html")),
    path("api/test/", TestView.as_view(), name="test"),
    path("api/user/", include("backend.users.urls", namespace="users")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# if settings.DEBUG:
urlpatterns += staticfiles_urlpatterns()
