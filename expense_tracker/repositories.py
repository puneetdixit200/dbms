from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from .db import Database


DEFAULT_EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Rent",
    "Utilities",
    "Shopping",
    "Healthcare",
    "Education",
    "Entertainment",
]

DEFAULT_INCOME_CATEGORIES = ["Salary", "Freelance", "Gift", "Interest", "Other"]


def create_user(db: Database, username: str, email: str, password_hash: str) -> int:
    with db.transaction() as cursor:
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (username.strip(), email.strip().lower(), password_hash),
        )
        user_id = cursor.lastrowid

        for name in DEFAULT_EXPENSE_CATEGORIES:
            cursor.execute(
                "INSERT INTO categories (user_id, name, type) VALUES (%s, %s, 'expense')",
                (user_id, name),
            )
        for name in DEFAULT_INCOME_CATEGORIES:
            cursor.execute(
                "INSERT INTO categories (user_id, name, type) VALUES (%s, %s, 'income')",
                (user_id, name),
            )

    return int(user_id)


def find_user_for_login(db: Database, login: str) -> dict[str, Any] | None:
    with db.transaction() as cursor:
        cursor.execute(
            """
            SELECT id, username, email, password_hash
            FROM users
            WHERE username = %s OR email = %s
            LIMIT 1
            """,
            (login.strip(), login.strip().lower()),
        )
        return cursor.fetchone()


def get_user(db: Database, user_id: int) -> dict[str, Any] | None:
    with db.transaction() as cursor:
        cursor.execute(
            "SELECT id, username, email, created_at FROM users WHERE id = %s",
            (user_id,),
        )
        return cursor.fetchone()


def list_categories(db: Database, user_id: int, category_type: str) -> list[dict[str, Any]]:
    with db.transaction() as cursor:
        cursor.execute(
            """
            SELECT id, name, type
            FROM categories
            WHERE user_id = %s AND type = %s
            ORDER BY name
            """,
            (user_id, category_type),
        )
        return cursor.fetchall()


def create_category(db: Database, user_id: int, name: str, category_type: str) -> None:
    with db.transaction() as cursor:
        cursor.execute(
            """
            INSERT INTO categories (user_id, name, type)
            VALUES (%s, %s, %s)
            """,
            (user_id, name.strip(), category_type),
        )


def list_expenses(db: Database, user_id: int) -> list[dict[str, Any]]:
    with db.transaction() as cursor:
        cursor.execute(
            """
            SELECT
                e.id,
                e.category_id,
                e.amount,
                DATE_FORMAT(e.expense_date, '%%Y-%%m-%%d') AS expense_date,
                e.description,
                e.payment_method,
                c.name AS category_name
            FROM expenses e
            INNER JOIN categories c ON c.id = e.category_id
            WHERE e.user_id = %s
            ORDER BY e.expense_date DESC, e.id DESC
            """,
            (user_id,),
        )
        return cursor.fetchall()


def add_expense(
    db: Database,
    user_id: int,
    category_id: int,
    amount: Decimal,
    expense_date: date,
    description: str,
    payment_method: str,
) -> None:
    with db.transaction() as cursor:
        cursor.execute(
            "CALL sp_add_expense(%s, %s, %s, %s, %s, %s)",
            (user_id, category_id, amount, expense_date, description, payment_method),
        )


def update_expense(
    db: Database,
    expense_id: int,
    user_id: int,
    category_id: int,
    amount: Decimal,
    expense_date: date,
    description: str,
    payment_method: str,
) -> None:
    with db.transaction() as cursor:
        cursor.execute(
            "CALL sp_update_expense(%s, %s, %s, %s, %s, %s, %s)",
            (expense_id, user_id, category_id, amount, expense_date, description, payment_method),
        )


def delete_expense(db: Database, expense_id: int, user_id: int) -> None:
    with db.transaction() as cursor:
        cursor.execute("CALL sp_delete_expense(%s, %s)", (expense_id, user_id))


def list_incomes(db: Database, user_id: int) -> list[dict[str, Any]]:
    with db.transaction() as cursor:
        cursor.execute(
            """
            SELECT
                i.id,
                i.category_id,
                i.amount,
                DATE_FORMAT(i.income_date, '%%Y-%%m-%%d') AS income_date,
                i.source,
                i.notes,
                c.name AS category_name
            FROM incomes i
            INNER JOIN categories c ON c.id = i.category_id
            WHERE i.user_id = %s
            ORDER BY i.income_date DESC, i.id DESC
            """,
            (user_id,),
        )
        return cursor.fetchall()


def add_income(
    db: Database,
    user_id: int,
    category_id: int,
    amount: Decimal,
    income_date: date,
    source: str,
    notes: str,
) -> None:
    with db.transaction() as cursor:
        cursor.execute(
            "CALL sp_add_income(%s, %s, %s, %s, %s, %s)",
            (user_id, category_id, amount, income_date, source, notes),
        )


def update_income(
    db: Database,
    income_id: int,
    user_id: int,
    category_id: int,
    amount: Decimal,
    income_date: date,
    source: str,
    notes: str,
) -> None:
    with db.transaction() as cursor:
        cursor.execute(
            "CALL sp_update_income(%s, %s, %s, %s, %s, %s, %s)",
            (income_id, user_id, category_id, amount, income_date, source, notes),
        )


def delete_income(db: Database, income_id: int, user_id: int) -> None:
    with db.transaction() as cursor:
        cursor.execute("CALL sp_delete_income(%s, %s)", (income_id, user_id))


def get_monthly_report(db: Database, user_id: int, year: int, month: int) -> dict[str, Any]:
    with db.transaction() as cursor:
        cursor.execute("CALL sp_monthly_report(%s, %s, %s)", (user_id, year, month))
        summary = cursor.fetchall()

        expense_categories: list[dict[str, Any]] = []
        income_categories: list[dict[str, Any]] = []

        if cursor.nextset():
            expense_categories = cursor.fetchall()
        if cursor.nextset():
            income_categories = cursor.fetchall()

    if summary:
        monthly = summary[0]
    else:
        monthly = {
            "year_no": year,
            "month_no": month,
            "total_income": Decimal("0.00"),
            "total_expense": Decimal("0.00"),
            "balance": Decimal("0.00"),
        }

    return {
        "monthly": monthly,
        "expense_categories": expense_categories,
        "income_categories": income_categories,
    }

