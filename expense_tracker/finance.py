from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


MONEY = Decimal("0.01")


def to_money(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(MONEY, rounding=ROUND_HALF_UP)


def calculate_balance(total_income: Decimal | int | float | str, total_expense: Decimal | int | float | str) -> Decimal:
    return to_money(total_income) - to_money(total_expense)

