import logging

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)
logger.info("Loading urls.py")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html")),
]

# ilija
