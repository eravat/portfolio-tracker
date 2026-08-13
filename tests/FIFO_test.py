from types import SimpleNamespace   #used to create arbritary values without defining a class
from main import get_quantity_and_RPL
import pytest

fake_buy_transaction = SimpleNamespace(type="buy", quantity=10, price=100)
fake_sell_transaction = SimpleNamespace(type="sell", quantity=10, price=150)
fake_full_sell_transaction = SimpleNamespace(type="sell", quantity=15, price=150)
fake_large_sell_transaction = SimpleNamespace(type="sell", quantity=30, price=150)
fake_over_sell_transaction = SimpleNamespace(type="sell", quantity=100, price=150)


def test_buy():
    temp_list, total_quantity, realised_PL = get_quantity_and_RPL(fake_buy_transaction, [], 0, 0)
    assert temp_list == [{"quantity":10, "price":100}]
    assert total_quantity == 10
    assert realised_PL == 0

def test_sell():
    temp_list, total_quantity, realised_PL = get_quantity_and_RPL(fake_sell_transaction, [{"quantity": 15, "price": 100}], 15, 0)
    assert temp_list == [{"quantity":5, "price":100}]
    assert total_quantity == 5
    assert realised_PL == 500

def test_full_sell():
    temp_list, total_quantity, realised_PL = get_quantity_and_RPL(fake_full_sell_transaction, [{"quantity": 15, "price": 100}], 15, 0)
    assert temp_list == []
    assert total_quantity == 0
    assert realised_PL == 750


def test_multiple_sell():
    temp_list, total_quantity, realised_PL = get_quantity_and_RPL(fake_large_sell_transaction, [{"quantity": 15, "price": 100}, {"quantity": 10, "price": 115}, {"quantity": 5, "price": 130}], 30, 0)
    assert temp_list == []
    assert total_quantity == 0
    assert realised_PL == 1200

def test_over_sell():
    with pytest.raises(IndexError):
        get_quantity_and_RPL(fake_over_sell_transaction, [{"quantity": 15, "price": 100}, {"quantity": 10, "price": 115}, {"quantity": 5, "price": 130}], 30, 0)
    
