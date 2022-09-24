from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from app.contrib.mixins import TitleContextMixin


class DashboardView(LoginRequiredMixin, TitleContextMixin, TemplateView):
    template_name = "dashboard.html"
    title = "Dashboard"
