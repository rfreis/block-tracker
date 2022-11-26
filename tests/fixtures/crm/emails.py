import pytest

from tests.fixtures.utils import content_from_file


@pytest.fixture
def email_confirmed_transaction_html():
    content = content_from_file(
        "tests/fixtures/crm/data/email_confirmed_transaction.html"
    )
    return content


@pytest.fixture
def email_confirmed_transaction_txt():
    content = content_from_file(
        "tests/fixtures/crm/data/email_confirmed_transaction.txt"
    )
    return content
