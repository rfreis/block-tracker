from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from app.contrib.mixins import BaseContextMixin
from transaction.utils import get_transactions_from_user
from wallet.models import UserWallet


class TransactionListView(LoginRequiredMixin, BaseContextMixin, ListView):
    app = "transaction"
    page = "list"
    template_name = "transaction/list.html"
    title = "Transactions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_wallets"] = UserWallet.objects.filter(
            user=self.request.user
        ).values_list("id", flat=True)
        return context

    def get_queryset(self):
        return get_transactions_from_user(self.request.user)
