from django.contrib.auth import (
    views as auth_views,
    login as auth_login,
)
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import BaseCreateView

from app.contrib.mixins import BaseContextMixin

from accounts.forms import RegisterForm
from dashboard.utils import sync_user_balance


class LoginView(BaseContextMixin, auth_views.LoginView):
    template_name = "accounts/login.html"
    title = "Login"


class LogoutView(auth_views.LogoutView):
    next_page = "accounts:login"


class RegisterView(BaseContextMixin, BaseCreateView, TemplateResponseMixin):
    template_name = "accounts/register.html"
    title = "Register"
    form_class = RegisterForm
    success_url = reverse_lazy("dashboard:dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        sync_user_balance(user)
        auth_login(self.request, user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.GET.get("email")
        return context


class PasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "accounts/password_change_form.html"


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"


class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("accounts:password_reset_done")
    email_template_name = "accounts/password_reset_email.txt"
    html_email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    template_name = "accounts/password_reset_form.html"


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "accounts/password_reset_confirm.html"
    title = "Enter new password"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
