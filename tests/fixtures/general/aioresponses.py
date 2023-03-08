import pytest  # noqa: F401
from aioresponses import aioresponses as original_aioresponses


@pytest.fixture
def aioresponses():
    return original_aioresponses
