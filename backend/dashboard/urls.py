from django.urls import path


from .views import OrderView


app_name = "dashboard"

urlpatterns = [
    path("donations/", OrderView.as_view(), name="order"),
]
