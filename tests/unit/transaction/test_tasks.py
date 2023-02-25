import pytest

from transaction.tasks import (
    new_confirmed_transactions,
    new_address,
    new_extended_public_key,
)


@pytest.mark.usefixtures(
    "db",
    "user_wallet_single_bitcoin_address_one",
    "user_wallet_bitcoin_xpub_one_user_two",
)
def test_new_confirmed_transactions(
    mocker, user_one, user_two, transaction_single_bitcoin_address_one
):
    mock_send_confirmed_transaction = mocker.patch(
        "transaction.tasks.send_confirmed_transaction",
    )

    new_confirmed_transactions([transaction_single_bitcoin_address_one.id])

    assert mock_send_confirmed_transaction.call_args_list[0][0] == (
        user_one,
        transaction_single_bitcoin_address_one,
    )
    assert mock_send_confirmed_transaction.call_args_list[1][0] == (
        user_two,
        transaction_single_bitcoin_address_one,
    )


@pytest.mark.usefixtures(
    "db",
    "user_wallet_single_bitcoin_address_one",
    "user_wallet_bitcoin_xpub_one",
    "user_two",
)
def test_new_confirmed_transactions_only_user_one(
    mocker, user_one, transaction_single_bitcoin_address_one
):
    mock_send_confirmed_transaction = mocker.patch(
        "transaction.tasks.send_confirmed_transaction",
    )

    new_confirmed_transactions([transaction_single_bitcoin_address_one.id])

    mock_send_confirmed_transaction.assert_called_once_with(
        user_one, transaction_single_bitcoin_address_one
    )


@pytest.mark.usefixtures("db", "user_wallet_single_bitcoin_address_one", "user_two")
def test_new_address(mocker, user_one, single_bitcoin_address_one):
    mock_sync_transactions_from_address = mocker.patch(
        "transaction.tasks.sync_transactions_from_address",
    )
    mock_sync_user_balance = mocker.patch(
        "transaction.tasks.sync_user_balance",
    )

    new_address(single_bitcoin_address_one.id)

    mock_sync_transactions_from_address.assert_called_once_with(
        single_bitcoin_address_one
    )
    mock_sync_user_balance.assert_called_once_with(user_one)


@pytest.mark.usefixtures("db", "user_wallet_bitcoin_xpub_one", "user_two")
@pytest.mark.usefixtures("db")
def test_new_extended_public_key(mocker, user_one, xpublic_key_bitcoin_one):
    mock_sync_transactions_from_extended_public_key = mocker.patch(
        "transaction.tasks.sync_transactions_from_extended_public_key",
    )
    mock_sync_user_balance = mocker.patch(
        "transaction.tasks.sync_user_balance",
    )

    new_extended_public_key(xpublic_key_bitcoin_one.id)

    mock_sync_transactions_from_extended_public_key.assert_called_once_with(
        xpublic_key_bitcoin_one
    )
    mock_sync_user_balance.assert_called_once_with(user_one)
