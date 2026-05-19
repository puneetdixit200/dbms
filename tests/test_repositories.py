from contextlib import contextmanager
from decimal import Decimal

from expense_tracker.repositories import get_monthly_report


class FakeCursor:
    def __init__(self):
        self.index = 0
        self.result_sets = [
            [{"total_income": Decimal("100.00"), "total_expense": Decimal("35.00"), "balance": Decimal("65.00")}],
            [{"category_name": "Food", "total_amount": Decimal("35.00")}],
            [{"category_name": "Salary", "total_amount": Decimal("100.00")}],
            [],
        ]

    def execute(self, statement, params):
        self.statement = statement
        self.params = params

    def fetchall(self):
        return self.result_sets[self.index]

    def nextset(self):
        if self.index + 1 < len(self.result_sets):
            self.index += 1
            return True
        return None


class FakeDb:
    def __init__(self):
        self.cursor = FakeCursor()

    @contextmanager
    def transaction(self):
        yield self.cursor


def test_get_monthly_report_consumes_all_stored_procedure_result_sets():
    db = FakeDb()

    report = get_monthly_report(db, user_id=1, year=2026, month=5)

    assert report["monthly"]["balance"] == Decimal("65.00")
    assert report["expense_categories"][0]["category_name"] == "Food"
    assert report["income_categories"][0]["category_name"] == "Salary"
    assert db.cursor.index == 3

