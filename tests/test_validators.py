from decimal import Decimal

from expense_tracker.validators import parse_iso_date, parse_positive_money, validate_month, validate_registration


def test_registration_requires_valid_user_details():
    errors = validate_registration("ab", "wrong-email", "123")

    assert "Username must be at least 3 characters." in errors
    assert "Enter a valid email address." in errors
    assert "Password must be at least 6 characters." in errors


def test_parse_positive_money_accepts_decimal_amount():
    amount, error = parse_positive_money("250.50")

    assert error is None
    assert amount == Decimal("250.50")


def test_parse_positive_money_rejects_zero():
    amount, error = parse_positive_money("0")

    assert amount is None
    assert error == "Amount must be greater than zero."


def test_parse_iso_date_accepts_yyyy_mm_dd():
    parsed, error = parse_iso_date("2026-05-19")

    assert error is None
    assert parsed.year == 2026
    assert parsed.month == 5
    assert parsed.day == 19


def test_validate_month_rejects_invalid_month():
    year, month, errors = validate_month("2026", "13")

    assert year == 2026
    assert month == 13
    assert errors == ["Month must be between 1 and 12."]

