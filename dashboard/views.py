from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from app.contrib.mixins import BaseContextMixin


class DashboardView(LoginRequiredMixin, BaseContextMixin, TemplateView):
    app = "dashboard"
    page = "dashboard"
    template_name = "dashboard.html"
    title = "Dashboard"
