# Personal Expense Tracker Using DBMS

## Abstract

Personal Expense Tracker is a mini DBMS project that helps a user record income, expenses, and categories. It calculates monthly income, monthly expense, and balance. The project uses a Python Flask backend, HTML/CSS/JavaScript frontend, and MySQL database.

## Objectives

- Provide user login and registration.
- Allow users to add, edit, and delete expenses.
- Track income records separately from expenses.
- Classify income and expenses using categories.
- Generate monthly reports and balance calculations.
- Demonstrate DBMS concepts including keys, joins, normalization, triggers, views, and stored procedures.

## Scope

The project is designed for a single-user-per-session web app. Each registered user has private categories, income records, expense records, and monthly balances.

## Modules

### Authentication Module

Users can register with username, email, and password. Passwords are stored as hashes using Werkzeug security helpers.

### Expense Module

Users can add, edit, and delete expense records. Each expense has category, amount, date, payment method, and description.

### Income Module

Users can add, edit, and delete income records. Each income record has category, amount, date, source, and notes.

### Category Module

Default income and expense categories are added during registration. Users can add more categories.

### Report Module

The report page displays monthly income, expenses, balance, expense category totals, and income category totals.

## ER Diagram

See [ER_DIAGRAM.md](ER_DIAGRAM.md).

## Database Tables

### users

Stores login and profile information.

Primary key: `id`

Unique keys: `username`, `email`

### categories

Stores user-specific income and expense categories.

Primary key: `id`

Foreign key: `user_id` references `users(id)`

Unique key: `(user_id, type, name)`

### expenses

Stores expense transactions.

Primary key: `id`

Foreign keys:

- `user_id` references `users(id)`
- `category_id` references `categories(id)`

### incomes

Stores income transactions.

Primary key: `id`

Foreign keys:

- `user_id` references `users(id)`
- `category_id` references `categories(id)`

### monthly_balances

Stores monthly totals maintained by triggers.

Composite primary key: `(user_id, year_no, month_no)`

## Joins Used

Expense list:

```sql
SELECT e.id, e.expense_date, c.name AS category, e.description, e.amount
FROM expenses e
INNER JOIN categories c ON c.id = e.category_id
WHERE e.user_id = 1;
```

Income list:

```sql
SELECT i.id, i.income_date, c.name AS category, i.source, i.amount
FROM incomes i
INNER JOIN categories c ON c.id = i.category_id
WHERE i.user_id = 1;
```

## Views

`v_monthly_financial_summary`

Shows monthly income, expenses, and balance with username.

`v_expense_category_summary`

Shows month-wise expense totals grouped by category.

`v_income_category_summary`

Shows month-wise income totals grouped by category.

## Triggers

The database includes triggers for:

- `expenses` after insert, update, delete
- `incomes` after insert, update, delete

Each trigger calls `sp_recalculate_monthly_balance`, so reports stay updated after every transaction change.

## Stored Procedures

- `sp_add_expense`
- `sp_update_expense`
- `sp_delete_expense`
- `sp_add_income`
- `sp_update_income`
- `sp_delete_income`
- `sp_monthly_report`
- `sp_recalculate_monthly_balance`

## Normalization

See [NORMALIZATION.md](NORMALIZATION.md).

## Sample Data

Sample data is available in `database/sample_data.sql`.

Demo login:

```text
Email: student@example.com
Password: sample123
```

## Testing

Automated tests cover:

- Flask login/register page loading
- Redirect protection for dashboard
- Input validation
- Balance calculation
- Presence of DBMS artifacts in the SQL schema

Run tests:

```powershell
pytest
```

## Future Enhancements

- Export reports to PDF or CSV
- Add budget limits by category
- Add charts for monthly trends
- Add password reset
- Add admin dashboard

