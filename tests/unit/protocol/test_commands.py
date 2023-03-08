import pytest  # noqa: F401
from django.core.management import CommandError, call_command

from protocol import ProtocolType


def test_wss_blockbook_command(mocker):
    class MockedProtocol:
        class MockedWSSBackend:
            start = None

        wss_backend = MockedWSSBackend()

    mock_start = mocker.patch.object(MockedProtocol.MockedWSSBackend, "start")
    mock_protocol = mocker.patch(
        "protocol.management.commands.wss_blockbook.Protocol",
        return_value=MockedProtocol(),
    )
    call_command("wss_blockbook", "BITCOIN")
    mock_protocol.assert_called_once_with(ProtocolType.BITCOIN)
    mock_start.assert_called_once()


def test_wss_blockbook_command_error():
    with pytest.raises(CommandError) as exc:
        call_command("wss_blockbook", "BITCOI")

    assert isinstance(exc.value, CommandError)
    assert str(exc.value) == "ProtocolType attr BITCOI invalid"
