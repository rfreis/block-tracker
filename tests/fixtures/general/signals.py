# This code was taken from:
# https://github.com/cameronmaske/django-drf-testing/blob/signals-example/tests/intergration_tests/conftest.py
# There was no declared license when I copied from there

import pytest

from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed,
)


@pytest.fixture(autouse=True)
def mute_signals(request):
    if "enable_signals" in request.keywords:
        return

    signals = [pre_save, post_save, pre_delete, post_delete, m2m_changed]
    restore = {}
    for signal in signals:
        # Temporally remove the signal's receivers (aka attached functions)
        restore[signal] = signal.receivers
        signal.receivers = []

    def restore_signals():
        # When the test tears down, restore the signals.
        for signal, receivers in restore.items():
            signal.receivers = receivers

    request.addfinalizer(restore_signals)
