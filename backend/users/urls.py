from django.urls import path

from .views import CustomUserCreate, TestCase

app_name = "users"

urlpatterns = [
    path("register/", CustomUserCreate.as_view(), name="create_user"),
    path("test/", TestCase.as_view(), name="test_case"),
]
