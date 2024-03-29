from datetime import datetime, timezone
from decimal import Decimal

import pytest  # noqa: F401

from protocol.constants import ProtocolType
from transaction.models import Transaction


@pytest.fixture
@pytest.mark.usefixtures("db")
def transaction_single_bitcoin_address_one(
    single_bitcoin_address_one, derived_bitcoin_address_one
):
    details = {
        "value_input": "0.00560766",
        "value_output": "0.00494962",
        "fee": "0.00065804",
        "value_input_usd": "49.972093328644915578",
        "value_output_usd": "44.108036610872885846",
        "fee_usd": "5.864056717772029732",
        "asset_name": "BTC",
        "block_hash": "000000000000000000605d39da6de74631bb1bbcdfb4703cb7f301e236ced12b",
        "inputs": [
            {
                "address": "3EEAuMT9VeteN4mTcC6NbubSEx94Rfq8C1",
                "amount_usd": "3.11275152197095919",
                "asset_name": "BTC",
                "amount_asset": "0.0003493",
            },
            {
                "address": "32JnwuVY4aLsPxW9VphZ7CRFwVuCQ2Y2dK",
                "amount_usd": "20.70207002774330173",
                "asset_name": "BTC",
                "amount_asset": "0.0023231",
            },
            {
                "address": "1PGr6CbRZuVDWVjhqm54WmAenCJyDAG22v",
                "amount_usd": "26.157271778930654658",
                "asset_name": "BTC",
                "amount_asset": "0.00293526",
            },
        ],
        "outputs": [
            {
                "address": "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
                "amount_usd": "6.005926183073425868",
                "asset_name": "BTC",
                "amount_asset": "0.00067396",
            },
            {
                "address": "3PPN46QdkkLBs8KEua5v2qPZGy54CYAXTs",
                "amount_usd": "12.371961982530609139",
                "asset_name": "BTC",
                "amount_asset": "0.00138833",
            },
            {
                "address": "17opNHjQAqBheBubbxRgRQAPrmR6ePsB8k",
                "amount_usd": "25.730148445268850839",
                "asset_name": "BTC",
                "amount_asset": "0.00288733",
            },
        ],
    }
    transaction = Transaction.objects.create(
        tx_id="a0a7e1bb6460bffed958bc80d74966be14fdec09608408de351053d1e8d653a1",
        block_id=508998,
        block_time=datetime(2018, 2, 13, 13, 52, 16, tzinfo=timezone.utc),
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=True,
        details=details,
    )
    transaction.inputdata.create(
        amount_asset=Decimal("0.00034930"),
        amount_usd=Decimal("3.112751521970959190"),
        asset_name="BTC",
        address=derived_bitcoin_address_one,
        vin_vout=0,
    )
    transaction.outputdata.create(
        amount_asset=Decimal("0.00288733"),
        amount_usd=Decimal("25.730148445268850839"),
        asset_name="BTC",
        address=single_bitcoin_address_one,
        vin_vout=2,
    )

    yield transaction

    transaction.inputdata.all().delete()
    transaction.outputdata.all().delete()
    transaction.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def transaction_derived_bitcoin_address_three(
    derived_bitcoin_address_three, derived_bitcoin_address_one
):
    details = {
        "value_input": "0.00067396",
        "value_output": "0.00065348",
        "fee": "0.00002048",
        "asset_name": "BTC",
        "block_hash": "00000000000000000006a6ffa1419f555e3bf7762b856c66443a2bcfcd2c83b1",
        "inputs": [
            {
                "address": "1JEYhhAGC2JkLJhdnC1tWk2CtH64sX2Ur8",
                "asset_name": "BTC",
                "amount_asset": "0.00067396",
            }
        ],
        "outputs": [
            {
                "address": "193P6LtvS4nCnkDvM9uXn1gsSRqh4aDAz7",
                "asset_name": "BTC",
                "amount_asset": "0.00065348",
            }
        ],
    }
    transaction = Transaction.objects.create(
        tx_id="b62aa5203fa27495ea431b91a5090aab741c8c39cc03ec4c1f4f4e157507595f",
        block_id=509003,
        block_time=datetime(2018, 2, 13, 14, 29, tzinfo=timezone.utc),
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=True,
        details=details,
    )
    transaction.inputdata.create(
        amount_asset=Decimal("0.00067396"),
        asset_name="BTC",
        address=derived_bitcoin_address_three,
        vin_vout=0,
    )
    transaction.outputdata.create(
        amount_asset=Decimal("0.00065348"),
        asset_name="BTC",
        address=derived_bitcoin_address_one,
        vin_vout=0,
    )

    yield transaction

    transaction.inputdata.all().delete()
    transaction.outputdata.all().delete()
    transaction.delete()


@pytest.fixture
@pytest.mark.usefixtures("db")
def transactions_balance(
    single_bitcoin_address_one,
    derived_bitcoin_address_one,
    derived_bitcoin_address_two,
):
    transaction_1 = Transaction.objects.create(
        tx_id="1",
        block_id=10,
        block_time=datetime(2022, 1, 1, 12, 00, tzinfo=timezone.utc),
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=True,
    )
    transaction_1.outputdata.create(
        amount_asset=Decimal("0.25"),
        asset_name="BTC",
        address=derived_bitcoin_address_one,
    )
    transaction_2 = Transaction.objects.create(
        tx_id="2",
        block_id=20,
        block_time=datetime(2022, 2, 1, 12, 00, tzinfo=timezone.utc),
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=True,
    )
    transaction_2.outputdata.create(
        amount_asset=Decimal("0.5"),
        asset_name="BTC",
        address=derived_bitcoin_address_one,
    )
    transaction_3 = Transaction.objects.create(
        tx_id="3",
        block_id=21,
        block_time=datetime(2022, 2, 1, 14, 00, tzinfo=timezone.utc),
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=True,
    )
    transaction_3.inputdata.create(
        amount_asset=Decimal("0.4"),
        asset_name="BTC",
        address=derived_bitcoin_address_one,
    )
    transaction_4 = Transaction.objects.create(
        tx_id="4",
        block_id=40,
        block_time=datetime(2022, 5, 1, 12, 00, tzinfo=timezone.utc),
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=True,
    )
    transaction_4.outputdata.create(
        amount_asset=Decimal("2.5"),
        asset_name="BTC",
        address=derived_bitcoin_address_two,
    )
    transaction_5 = Transaction.objects.create(
        tx_id="5",
        block_id=50,
        block_time=datetime(2022, 5, 31, 12, 00, tzinfo=timezone.utc),
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=True,
    )
    transaction_5.outputdata.create(
        amount_asset=Decimal("1"),
        asset_name="BTC",
        address=single_bitcoin_address_one,
    )
    transaction_6 = Transaction.objects.create(
        tx_id="6",
        block_id=60,
        block_time=datetime(2022, 6, 1, 12, 00, tzinfo=timezone.utc),
        protocol_type=ProtocolType.BITCOIN,
        is_confirmed=False,
    )
    transaction_6.outputdata.create(
        amount_asset=Decimal("100"),
        asset_name="BTC",
        address=derived_bitcoin_address_one,
    )
    transactions = [
        transaction_1,
        transaction_2,
        transaction_3,
        transaction_4,
        transaction_5,
        transaction_6,
    ]

    yield transactions

    for transaction in transactions:
        transaction.inputdata.all().delete()
        transaction.outputdata.all().delete()
        transaction.delete()
