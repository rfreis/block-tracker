import pytest
from freezegun import freeze_time

from django.core import mail

from crm.utils import send_confirmed_transaction


@freeze_time("2018-02-13 13:52:16")
@pytest.mark.usefixtures("db")
def test_send_confirmed_transaction(
    user_one,
    transaction_single_bitcoin_address_one,
    email_confirmed_transaction_html,
    email_confirmed_transaction_txt,
):
    send_confirmed_transaction(user_one, transaction_single_bitcoin_address_one)

    assert len(mail.outbox) == 1

    sent_email = mail.outbox[0]
    assert sent_email.subject == "Bitcoin: New confirmed transaction - 13/02/18"
    assert sent_email.to == ["user_one@email.com"]

    txt_content = sent_email.message().get_payload()[0].get_payload()
    html_content = sent_email.message().get_payload()[1].get_payload()

    assert email_confirmed_transaction_html == html_content
    assert email_confirmed_transaction_txt == txt_content
