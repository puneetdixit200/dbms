from decimal import Decimal

from expense_tracker.finance import calculate_balance, to_money


def test_to_money_rounds_to_two_places():
    assert to_money("10.236") == Decimal("10.24")


def test_calculate_balance_subtracts_expenses_from_income():
    assert calculate_balance("51950.00", "21100.00") == Decimal("30850.00")

