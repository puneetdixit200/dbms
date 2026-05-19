# Normalization

## Unnormalized Data Problem

A simple spreadsheet-like design might store user, category, expense, and income details in one table:

```text
username, email, password, expense_category, expense_amount, income_category, income_amount, month
```

This causes repeated user data, repeated category names, update anomalies, and difficulty separating income from expenses.

## First Normal Form (1NF)

The design satisfies 1NF because:

- Each column stores atomic values.
- Repeating groups are removed.
- Expense and income records are stored as separate rows.

Examples:

- `expenses.amount` stores one amount only.
- `categories.name` stores one category name only.

## Second Normal Form (2NF)

The design satisfies 2NF because:

- Tables with single-column primary keys have all non-key columns depending on the whole key.
- `monthly_balances` uses a composite primary key `(user_id, year_no, month_no)`, and its totals depend on that full key.

Examples:

- In `expenses`, amount, date, description, and payment method depend on `expenses.id`.
- In `monthly_balances`, totals depend on the user, year, and month together.

## Third Normal Form (3NF)

The design satisfies 3NF because:

- Non-key attributes do not depend on other non-key attributes.
- Category names are stored in `categories`, not repeated in `expenses` or `incomes`.
- User login details are stored in `users`, not repeated in transaction tables.

## Final Tables

- `users`
- `categories`
- `expenses`
- `incomes`
- `monthly_balances`

## Benefits

- Less duplicate data
- Cleaner joins
- Easier category updates
- Better report accuracy
- Trigger-based balance recalculation from normalized source tables

