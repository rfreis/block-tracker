from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )
    first_name = forms.CharField(
        max_length=255, help_text="Required. Inform your first name."
    )
    last_name = forms.CharField(
        max_length=255, help_text="Required. Inform your last name."
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def _post_clean(self):
        super()._post_clean()
        self.instance.username = self.instance.email
