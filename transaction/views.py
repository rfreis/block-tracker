from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.list import ListView

from app.contrib.mixins import BaseContextMixin
from transaction.models import Transaction
from wallet.models import UserWallet


class TransactionListView(LoginRequiredMixin, BaseContextMixin, ListView):
    app = "transaction"
    page = "list"
    queryset = Transaction.objects.filter(is_orphan=False).order_by("-block_time")
    template_name = "transaction/list.html"
    title = "Transactions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_wallets"] = UserWallet.objects.filter(
            user=self.request.user
        ).values_list("id", flat=True)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(inputs__user_wallet__user=self.request.user)
            | Q(inputs__extended_public_key__user_wallet__user=self.request.user)
            | Q(outputs__user_wallet__user=self.request.user)
            | Q(outputs__extended_public_key__user_wallet__user=self.request.user)
        )
        return queryset.distinct()
