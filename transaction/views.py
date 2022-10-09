from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.list import ListView

from app.contrib.mixins import BaseContextMixin
from transaction.models import Transaction


class TransactionListView(LoginRequiredMixin, BaseContextMixin, ListView):
    app = "transaction"
    page = "list"
    queryset = (
        Transaction.objects.select_related("address")
        .prefetch_related("address__user_wallet", "address__public_key__user_wallet")
        .order_by("-id")
    )
    template_name = "transaction/list.html"
    title = "Transactions"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(address__user_wallet__user=self.request.user)
            | Q(address__public_key__user_wallet__user=self.request.user)
        )
        return queryset
