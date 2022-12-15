from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from app.contrib.mixins import BaseContextMixin
from rate.utils import get_usd_rate
from wallet.forms import CreateUserWalletForm
from wallet.models import UserWallet


class WalletListView(LoginRequiredMixin, BaseContextMixin, ListView):
    app = "wallet"
    page = "list"
    queryset = UserWallet.objects.select_related("extended_public_key", "address")
    template_name = "wallet/list.html"
    title = "Wallets"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class WalletCreateView(LoginRequiredMixin, BaseContextMixin, CreateView):
    app = "wallet"
    form_class = CreateUserWalletForm
    page = "create"
    success_url = reverse_lazy("wallet:list")
    template_name = "wallet/create.html"
    title = "Add Wallet"

    def form_valid(self, form):
        form.add_user(self.request.user)
        return super().form_valid(form)
