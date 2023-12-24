from django.urls import path

from .views import BlacklistTokenUpdateView, CustomUserCreate, UserProfileView

app_name = "users"

urlpatterns = [
    path("register/", CustomUserCreate.as_view(), name="create_user"),
    path("userStatus/", UserProfileView.as_view(), name="user_profile"),
    path("logout/blacklist/", BlacklistTokenUpdateView.as_view(), name="blacklist"),
]
