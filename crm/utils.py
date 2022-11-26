import logging
from datetime import datetime
from django.conf import settings

from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def send_confirmed_transaction(user, transaction):
    context = {
        "user": user,
        "transaction": transaction,
    }
    today = datetime.utcnow().strftime("%d/%m/%y")
    subject = f"{transaction.get_protocol_type_display()}: New confirmed transaction - {today}"
    html_template = "crm/emails/confirmed_transaction.html"
    body_html = render_to_string(html_template, context)
    txt_template = "crm/emails/confirmed_transaction.txt"
    body_txt = render_to_string(txt_template, context)

    user.email_user(
        subject,
        body_txt,
        settings.DEFAULT_FROM_EMAIL,
        html_message=body_html,
    )
    logger.debug(
        f"New confirmed transaction #%s email sent to user #%s"
        % (transaction.id, user.id)
    )
