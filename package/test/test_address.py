import pytest
import common
from finlaw.list_form import Address


def test_address_eq():
    assert Address("15.1.12") == Address("15.1.12")
    assert Address("15.1.12") == Address((15, 1, 12))
    assert Address((15, 1, 12)) == Address((15, 1, 12))


def test_address_neq():
    assert Address("15.1.12") != Address("15.1.13")