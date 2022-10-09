from django.urls import path
from . import views

app_name = "transaction"


urlpatterns = [
    path("", views.TransactionListView.as_view(), name="list"),
]
