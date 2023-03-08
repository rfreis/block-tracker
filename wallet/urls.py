from django.urls import path

from . import views

app_name = "wallet"


urlpatterns = [
    path("", views.WalletListView.as_view(), name="list"),
    path("add/", views.WalletCreateView.as_view(), name="create"),
]
