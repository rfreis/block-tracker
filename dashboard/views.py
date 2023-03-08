from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from app.contrib.mixins import BaseContextMixin
from dashboard.models import UserBalance
from dashboard.utils import get_balance_rate
from transaction.utils import get_transactions_from_user
from wallet.models import UserWallet


class DashboardView(LoginRequiredMixin, BaseContextMixin, TemplateView):
    app = "dashboard"
    page = "dashboard"
    template_name = "dashboard.html"
    title = "Dashboard"
    dominance_colors_bg = ["#4e73df", "#1cc88a", "#36b9cc"]
    dominance_colors_bg_hover = ["#2e59d9", "#17a673", "#2c9faf"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_wallets"] = UserWallet.objects.filter(
            user=self.request.user
        ).values_list("id", flat=True)
        user_balances = UserBalance.objects.filter(user=self.request.user)
        context["monthly_amount_usd"] = self.get_monthly_amount_usd(user_balances)
        context["current_user_balance"] = context["monthly_amount_usd"][11]["balance"]
        context["current_usd_amount"] = context["monthly_amount_usd"][11][
            "total_amount_usd"
        ]
        context["last_month_user_balance"] = context["monthly_amount_usd"][10][
            "balance"
        ]
        context["last_month_usd_amount"] = context["monthly_amount_usd"][10][
            "total_amount_usd"
        ]
        context["performance_vs_last_month"] = str(
            Decimal(context["current_usd_amount"])
            - Decimal(context["last_month_usd_amount"])
        )
        if Decimal(context["last_month_usd_amount"]) == 0:
            context["performance_vs_last_month_pct"] = "0"
        else:
            context["performance_vs_last_month_pct"] = str(
                (
                    Decimal(context["performance_vs_last_month"])
                    / Decimal(context["last_month_usd_amount"])
                )
                * 100
            )
        context["asset_dominance"] = self.get_asset_dominance(
            context["monthly_amount_usd"][11]["amount_usd_by_asset"],
            context["monthly_amount_usd"][11]["total_amount_usd"],
        )
        transactions = get_transactions_from_user(self.request.user)
        context["transactions_count"] = transactions.count()
        context["last_transactions"] = transactions[:10]
        return context

    def get_monthly_amount_usd(self, user_balances):
        content = []
        for index in range(12):
            time_reference = datetime.utcnow()
            if index:
                time_reference -= relativedelta(months=index)
            user_balance = user_balances.order_by("-date")[:12][index]
            total_amount_usd, amount_usd_by_asset = get_balance_rate(
                user_balance.balance, time_reference
            )
            content.append(
                {
                    "date": time_reference.strftime("%m/%Y"),
                    "total_amount_usd": total_amount_usd,
                    "amount_usd_by_asset": amount_usd_by_asset,
                    "balance": user_balance.balance,
                }
            )
        return list(reversed(content))

    def get_asset_dominance(self, amount_usd_by_asset, total_amount_usd):
        content = []
        total_amount_usd = Decimal(total_amount_usd)
        for index, (asset_name, amount_usd) in enumerate(amount_usd_by_asset.items()):
            content.append(
                {
                    "asset_name": asset_name,
                    "amount_usd": str(amount_usd),
                    "background_color": self.dominance_colors_bg[index],
                    "background_color_hover": self.dominance_colors_bg_hover[index],
                },
            )
        return content
