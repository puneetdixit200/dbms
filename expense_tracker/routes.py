from __future__ import annotations

from datetime import date
from functools import wraps
from typing import Any, Callable

from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import repositories
from .db import DatabaseError
from .finance import calculate_balance
from .validators import clean_text, parse_iso_date, parse_positive_money, validate_month, validate_registration


bp = Blueprint("main", __name__)


def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please log in first.", "warning")
            return redirect(url_for("main.login"))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user() -> None:
    user_id = session.get("user_id")
    g.user = None
    if user_id is None:
        return

    try:
        g.user = repositories.get_user(current_app.db, int(user_id))  # type: ignore[attr-defined]
    except DatabaseError:
        session.clear()
        flash("Database connection failed. Check MySQL and .env settings.", "danger")


@bp.route("/")
def index():
    if g.user:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("main.login"))


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        errors = validate_registration(username, email, password)
        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            try:
                user_id = repositories.create_user(
                    current_app.db,  # type: ignore[attr-defined]
                    username,
                    email,
                    generate_password_hash(password),
                )
                session.clear()
                session["user_id"] = user_id
                flash("Account created. Default income and expense categories were added.", "success")
                return redirect(url_for("main.dashboard"))
            except Exception:
                flash("Could not register. Username or email may already exist.", "danger")

    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        login_value = request.form.get("login", "")
        password = request.form.get("password", "")

        try:
            user = repositories.find_user_for_login(current_app.db, login_value)  # type: ignore[attr-defined]
        except DatabaseError:
            flash("Database connection failed. Check MySQL and .env settings.", "danger")
            return render_template("login.html")

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid username/email or password.", "danger")
        else:
            session.clear()
            session["user_id"] = user["id"]
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.dashboard"))

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("main.login"))


@bp.route("/dashboard")
@login_required
def dashboard():
    today = date.today()
    year, month, errors = validate_month(
        request.args.get("year", today.year),
        request.args.get("month", today.month),
    )
    for error in errors:
        flash(error, "danger")

    report = repositories.get_monthly_report(current_app.db, g.user["id"], year, month)  # type: ignore[attr-defined]
    expenses = repositories.list_expenses(current_app.db, g.user["id"])[:5]  # type: ignore[attr-defined]
    incomes = repositories.list_incomes(current_app.db, g.user["id"])[:5]  # type: ignore[attr-defined]
    monthly = report["monthly"]
    monthly["balance"] = calculate_balance(monthly["total_income"], monthly["total_expense"])

    return render_template(
        "dashboard.html",
        report=report,
        expenses=expenses,
        incomes=incomes,
        selected_year=year,
        selected_month=month,
    )


@bp.route("/expenses", methods=("GET", "POST"))
@login_required
def expenses():
    if request.method == "POST":
        category_id = request.form.get("category_id", type=int)
        amount, amount_error = parse_positive_money(request.form.get("amount", ""))
        expense_date, date_error = parse_iso_date(request.form.get("expense_date", ""))
        description = clean_text(request.form.get("description"), 255)
        payment_method = clean_text(request.form.get("payment_method"), 50) or "Cash"

        if amount_error:
            flash(amount_error, "danger")
        if date_error:
            flash(date_error, "danger")
        if category_id is None:
            flash("Select an expense category.", "danger")

        if category_id and amount and expense_date:
            repositories.add_expense(
                current_app.db,  # type: ignore[attr-defined]
                g.user["id"],
                category_id,
                amount,
                expense_date,
                description,
                payment_method,
            )
            flash("Expense added.", "success")
            return redirect(url_for("main.expenses"))

    return render_expenses_page()


@bp.route("/expenses/<int:expense_id>/edit", methods=("POST",))
@login_required
def edit_expense(expense_id: int):
    category_id = request.form.get("category_id", type=int)
    amount, amount_error = parse_positive_money(request.form.get("amount", ""))
    expense_date, date_error = parse_iso_date(request.form.get("expense_date", ""))
    description = clean_text(request.form.get("description"), 255)
    payment_method = clean_text(request.form.get("payment_method"), 50) or "Cash"

    if amount_error or date_error or category_id is None:
        flash(amount_error or date_error or "Select an expense category.", "danger")
        return redirect(url_for("main.expenses"))

    repositories.update_expense(
        current_app.db,  # type: ignore[attr-defined]
        expense_id,
        g.user["id"],
        category_id,
        amount,
        expense_date,
        description,
        payment_method,
    )
    flash("Expense updated.", "success")
    return redirect(url_for("main.expenses"))


@bp.route("/expenses/<int:expense_id>/delete", methods=("POST",))
@login_required
def delete_expense(expense_id: int):
    repositories.delete_expense(current_app.db, expense_id, g.user["id"])  # type: ignore[attr-defined]
    flash("Expense deleted.", "info")
    return redirect(url_for("main.expenses"))


def render_expenses_page():
    categories = repositories.list_categories(current_app.db, g.user["id"], "expense")  # type: ignore[attr-defined]
    expenses = repositories.list_expenses(current_app.db, g.user["id"])  # type: ignore[attr-defined]
    return render_template("expenses.html", categories=categories, expenses=expenses)


@bp.route("/incomes", methods=("GET", "POST"))
@login_required
def incomes():
    if request.method == "POST":
        category_id = request.form.get("category_id", type=int)
        amount, amount_error = parse_positive_money(request.form.get("amount", ""))
        income_date, date_error = parse_iso_date(request.form.get("income_date", ""))
        source = clean_text(request.form.get("source"), 100)
        notes = clean_text(request.form.get("notes"), 255)

        if amount_error:
            flash(amount_error, "danger")
        if date_error:
            flash(date_error, "danger")
        if category_id is None:
            flash("Select an income category.", "danger")

        if category_id and amount and income_date:
            repositories.add_income(
                current_app.db,  # type: ignore[attr-defined]
                g.user["id"],
                category_id,
                amount,
                income_date,
                source,
                notes,
            )
            flash("Income added.", "success")
            return redirect(url_for("main.incomes"))

    return render_incomes_page()


@bp.route("/incomes/<int:income_id>/edit", methods=("POST",))
@login_required
def edit_income(income_id: int):
    category_id = request.form.get("category_id", type=int)
    amount, amount_error = parse_positive_money(request.form.get("amount", ""))
    income_date, date_error = parse_iso_date(request.form.get("income_date", ""))
    source = clean_text(request.form.get("source"), 100)
    notes = clean_text(request.form.get("notes"), 255)

    if amount_error or date_error or category_id is None:
        flash(amount_error or date_error or "Select an income category.", "danger")
        return redirect(url_for("main.incomes"))

    repositories.update_income(
        current_app.db,  # type: ignore[attr-defined]
        income_id,
        g.user["id"],
        category_id,
        amount,
        income_date,
        source,
        notes,
    )
    flash("Income updated.", "success")
    return redirect(url_for("main.incomes"))


@bp.route("/incomes/<int:income_id>/delete", methods=("POST",))
@login_required
def delete_income(income_id: int):
    repositories.delete_income(current_app.db, income_id, g.user["id"])  # type: ignore[attr-defined]
    flash("Income deleted.", "info")
    return redirect(url_for("main.incomes"))


def render_incomes_page():
    categories = repositories.list_categories(current_app.db, g.user["id"], "income")  # type: ignore[attr-defined]
    incomes = repositories.list_incomes(current_app.db, g.user["id"])  # type: ignore[attr-defined]
    return render_template("incomes.html", categories=categories, incomes=incomes)


@bp.route("/categories", methods=("POST",))
@login_required
def categories():
    category_type = request.form.get("type", "expense")
    name = clean_text(request.form.get("name"), 80)
    next_page = "main.expenses" if category_type == "expense" else "main.incomes"

    if category_type not in {"expense", "income"}:
        flash("Invalid category type.", "danger")
    elif not name:
        flash("Category name is required.", "danger")
    else:
        try:
            repositories.create_category(current_app.db, g.user["id"], name, category_type)  # type: ignore[attr-defined]
            flash("Category added.", "success")
        except Exception:
            flash("That category already exists.", "warning")

    return redirect(url_for(next_page))


@bp.route("/reports")
@login_required
def reports():
    today = date.today()
    year, month, errors = validate_month(
        request.args.get("year", today.year),
        request.args.get("month", today.month),
    )
    for error in errors:
        flash(error, "danger")

    report = repositories.get_monthly_report(current_app.db, g.user["id"], year, month)  # type: ignore[attr-defined]
    report["monthly"]["balance"] = calculate_balance(
        report["monthly"]["total_income"],
        report["monthly"]["total_expense"],
    )

    return render_template("reports.html", report=report, selected_year=year, selected_month=month)

