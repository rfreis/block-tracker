from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from app.contrib.mixins import BaseContextMixin


class LoginView(BaseContextMixin, auth_views.LoginView):
    template_name = "accounts/login.html"
    title = "Login"


class LogoutView(auth_views.LogoutView):
    next_page = "accounts:login"


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
