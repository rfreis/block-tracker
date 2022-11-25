import pytest
from datetime import datetime, timezone
from decimal import Decimal

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
        "block_hash": "000000000000000000605d39da6de74631bb1bbcdfb4703cb7f301e236ced12b",
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
        asset_name="BTC",
        address=derived_bitcoin_address_one,
    )
    transaction.outputdata.create(
        amount_asset=Decimal("0.00288733"),
        asset_name="BTC",
        address=single_bitcoin_address_one,
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
        "block_hash": "00000000000000000006a6ffa1419f555e3bf7762b856c66443a2bcfcd2c83b1",
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
    )
    transaction.outputdata.create(
        amount_asset=Decimal("0.00065348"),
        asset_name="BTC",
        address=derived_bitcoin_address_one,
    )

    yield transaction

    transaction.inputdata.all().delete()
    transaction.outputdata.all().delete()
    transaction.delete()
