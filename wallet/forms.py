from django import forms
from django.core.exceptions import ValidationError

from protocol import Protocol
from protocol.constants import ProtocolType
from wallet.models import PublicKey, Address, UserWallet
from wallet.constants import WalletType


def get_public_key_or_address_form(MyModel, validate_func_name):
    class MyForm(forms.ModelForm):
        class Meta:
            model = MyModel
            fields = [
                "hash",
                "protocol_type",
            ]

        def clean(self):
            super().clean()
            protocol_type = int(self.cleaned_data["protocol_type"])
            protocol = Protocol(protocol_type)
            hash = self.cleaned_data["hash"]
            validate_func = getattr(protocol, validate_func_name)
            if not validate_func(hash):
                raise ValidationError("Public Key is not valid")
            return self.cleaned_data

        def _post_clean(self):
            super()._post_clean()
            public_key = PublicKey.objects.filter(
                hash=self.cleaned_data["hash"],
                protocol_type=self.cleaned_data["protocol_type"],
            )
            if public_key:
                self.instance = public_key.first()

    return MyForm


class UserWalletForm(forms.ModelForm):
    class Meta:
        model = UserWallet
        fields = [
            "label",
            "public_key",
            "address",
            "wallet_type",
        ]


class CreateUserWalletForm(forms.Form):
    hash = forms.CharField(label="Public Key or Address")
    label = forms.CharField(label="Label")
    protocol_type = forms.ChoiceField(
        label="Protocol",
        choices=ProtocolType.choices,
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop("instance")
        super().__init__(*args, **kwargs)
        self.fields["protocol_type"].widget.attrs.update({"class": "form-control"})

    def add_user(self, user):
        self.user_wallet_form.instance.user = user

    def clean(self):
        super().clean()
        protocol_type = int(self.cleaned_data.pop("protocol_type"))
        hash = self.cleaned_data.pop("hash")
        PublicKeyForm = get_public_key_or_address_form(PublicKey, "validate_public_key")
        public_key_form = PublicKeyForm(
            {
                "protocol_type": protocol_type,
                "hash": hash,
            }
        )
        AddressForm = get_public_key_or_address_form(Address, "validate_address")
        address_form = AddressForm(
            {
                "protocol_type": protocol_type,
                "hash": hash,
            }
        )
        if public_key_form.is_valid():
            if not public_key_form.instance.id:
                public_key_form.save()
            self.user_wallet_form = UserWalletForm(
                {
                    "public_key": public_key_form.instance,
                    "wallet_type": WalletType.PUBLIC_KEY,
                    "label": self.cleaned_data["label"],
                }
            )
        elif address_form.is_valid():
            if not address_form.instance.id:
                address_form.save()
            self.user_wallet_form = UserWalletForm(
                {
                    "address": address_form.instance,
                    "wallet_type": WalletType.ADDRESS,
                    "label": self.cleaned_data["label"],
                }
            )
        else:
            self.add_error("hash", "The hash is invalid for the selected protocol.")
            return self.cleaned_data

        if not self.user_wallet_form.is_valid():
            errors = []
            for error in self.user_wallet_form.errors.values():
                errors.append(error)
            self.add_error(None, errors)
        return self.cleaned_data

    def save(self, commit=True):
        self.user_wallet_form.save(commit)
        return self.user_wallet_form.instance
