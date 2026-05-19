from pathlib import Path


SCHEMA = Path("database/schema.sql").read_text(encoding="utf-8").lower()
QUERIES = Path("database/queries.sql").read_text(encoding="utf-8").lower()


def test_schema_contains_required_tables():
    for table in ["users", "categories", "expenses", "incomes", "monthly_balances"]:
        assert f"create table {table}" in SCHEMA


def test_schema_contains_views_triggers_and_stored_procedures():
    for artifact in [
        "create view v_monthly_financial_summary",
        "create view v_expense_category_summary",
        "create trigger trg_expenses_after_insert",
        "create trigger trg_incomes_after_delete",
        "create procedure sp_add_expense",
        "create procedure sp_monthly_report",
    ]:
        assert artifact in SCHEMA


def test_query_examples_include_joins_and_procedure_calls():
    assert "inner join categories" in QUERIES
    assert "call sp_monthly_report" in QUERIES

