from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from email.utils import parseaddr


def clean_text(value: str | None, max_length: int) -> str:
    text = (value or "").strip()
    return text[:max_length]


def validate_registration(username: str, email: str, password: str) -> list[str]:
    errors: list[str] = []
    username = username.strip()
    email = email.strip()

    if len(username) < 3:
        errors.append("Username must be at least 3 characters.")
    if len(username) > 50:
        errors.append("Username must be 50 characters or less.")
    if "@" not in parseaddr(email)[1]:
        errors.append("Enter a valid email address.")
    if len(password) < 6:
        errors.append("Password must be at least 6 characters.")

    return errors


def parse_positive_money(value: str, field_name: str = "Amount") -> tuple[Decimal | None, str | None]:
    try:
        amount = Decimal(value.strip())
    except (InvalidOperation, AttributeError):
        return None, f"{field_name} must be a valid number."

    if amount <= 0:
        return None, f"{field_name} must be greater than zero."

    return amount.quantize(Decimal("0.01")), None


def parse_iso_date(value: str, field_name: str = "Date") -> tuple[date | None, str | None]:
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date(), None
    except (ValueError, AttributeError):
        return None, f"{field_name} must use YYYY-MM-DD format."


def validate_month(year_value: str | int, month_value: str | int) -> tuple[int, int, list[str]]:
    errors: list[str] = []
    try:
        year = int(year_value)
        month = int(month_value)
    except (TypeError, ValueError):
        return date.today().year, date.today().month, ["Year and month must be numbers."]

    if year < 2000 or year > 2100:
        errors.append("Year must be between 2000 and 2100.")
    if month < 1 or month > 12:
        errors.append("Month must be between 1 and 12.")

    return year, month, errors

