import logging

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

logger = logging.getLogger(__name__)
logger.info("Loading urls.py")

urlpatterns = [
    path("admin/", admin.site.urls),
]
