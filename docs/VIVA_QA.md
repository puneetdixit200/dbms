# Project Viva and Q&A

Use these questions to prepare for project review, viva, or presentation follow-up.

## Basic Project Questions

### 1. What is your project?

My project is Personal Expense Tracker Using DBMS. It is a web app where users can record income, record expenses, assign categories, and view monthly balance reports.

### 2. What problem does it solve?

It helps users understand how much money they earn, how much they spend, and how much balance remains each month.

### 3. Which technologies did you use?

I used HTML, CSS, and JavaScript for the frontend, Python Flask for the backend, and MySQL for the database.

### 4. Why did you choose Python Flask?

Flask is lightweight and simple for a mini project. It lets me create routes, handle forms, manage sessions, and connect to MySQL without extra complexity.

### 5. Why did you choose MySQL?

MySQL is a relational database. It supports tables, keys, joins, views, triggers, and stored procedures, which match the DBMS requirements of this project.

## Feature Questions

### 6. What can a user do after logging in?

The user can manage expenses, manage income, create categories, and view monthly reports.

### 7. Can users edit and delete old records?

Yes. The Expenses and Income pages include edit and delete actions for existing records.

### 8. How does the app calculate balance?

Balance equals total income minus total expense for a selected month.

### 9. Does each user have separate data?

Yes. Tables include `user_id`, so each user's categories, income, expenses, and monthly balances stay separate.

### 10. What sample login can the evaluator use?

The sample login is:

```text
Email: student@example.com
Password: sample123
```

## Database Design Questions

### 11. What are the main tables?

The main tables are `users`, `categories`, `expenses`, `incomes`, and `monthly_balances`.

### 12. What does the `users` table store?

It stores username, email, password hash, and account creation time.

### 13. What does the `categories` table store?

It stores category names such as Food, Rent, Salary, and Freelance. It also stores whether a category belongs to income or expense.

### 14. What does the `expenses` table store?

It stores amount, date, description, payment method, user id, and category id for each expense.

### 15. What does the `incomes` table store?

It stores amount, date, source, notes, user id, and category id for each income record.

### 16. What does the `monthly_balances` table store?

It stores monthly total income, total expense, and balance for each user.

### 17. What is the primary key of `monthly_balances`?

The primary key is composite: `(user_id, year_no, month_no)`.

### 18. Why did you use a composite key in `monthly_balances`?

A user should have only one balance row for a specific year and month. The composite key enforces that rule.

### 19. Which foreign keys did you use?

I used foreign keys from categories, expenses, incomes, and monthly balances to users. I also used foreign keys from expenses and incomes to categories.

### 20. Why are foreign keys important in this project?

Foreign keys prevent invalid records. For example, an expense cannot refer to a category that does not exist.

## Normalization Questions

### 21. Is your database normalized?

Yes. The database follows 1NF, 2NF, and 3NF.

### 22. How does it satisfy 1NF?

Each column stores atomic values. For example, one expense row stores one amount and one date.

### 23. How does it satisfy 2NF?

Non-key columns depend on the full primary key. In `monthly_balances`, totals depend on the user, year, and month together.

### 24. How does it satisfy 3NF?

Non-key columns do not depend on other non-key columns. Category names stay in `categories`, not inside every expense or income row.

### 25. Why not store category name directly in the expenses table?

That would repeat category names and create update problems. Storing `category_id` keeps the database cleaner.

## SQL and DBMS Concept Questions

### 26. Where did you use joins?

The app joins `expenses` with `categories` to display expense category names. It also joins `incomes` with `categories`.

### 27. Give one join example from the project.

```sql
SELECT e.id, e.expense_date, c.name AS category, e.amount
FROM expenses e
INNER JOIN categories c ON c.id = e.category_id
WHERE e.user_id = 1;
```

### 28. What is a view?

A view is a saved SQL query that behaves like a virtual table.

### 29. Which views did you create?

I created `v_monthly_financial_summary`, `v_expense_category_summary`, and `v_income_category_summary`.

### 30. Why did you use views?

Views make report queries cleaner. The backend can read summarized data without repeating long SQL every time.

### 31. What is a trigger?

A trigger is database logic that runs automatically after a table event such as insert, update, or delete.

### 32. Where did you use triggers?

I used triggers on `expenses` and `incomes` after insert, update, and delete.

### 33. Why did you use triggers?

Triggers recalculate monthly balances when the user changes income or expense records.

### 34. What is a stored procedure?

A stored procedure is a named SQL routine stored inside the database. The backend can call it with parameters.

### 35. Which stored procedures did you create?

The project includes procedures such as `sp_add_expense`, `sp_update_expense`, `sp_delete_expense`, `sp_add_income`, `sp_update_income`, `sp_delete_income`, `sp_monthly_report`, and `sp_recalculate_monthly_balance`.

### 36. Why use stored procedures here?

Stored procedures keep repeated database operations in one place and make backend code cleaner.

### 37. What happens when a user adds an expense?

The backend calls `sp_add_expense`. MySQL inserts the expense row. Then an expense trigger calls `sp_recalculate_monthly_balance`.

### 38. What happens when a user deletes an income record?

The delete procedure removes the row. Then the income delete trigger recalculates the monthly balance for that month.

## Backend Questions

### 39. How does Flask connect to MySQL?

The app uses `mysql-connector-python`. Database settings come from `.env`.

### 40. Where are the database settings stored?

They are stored in `.env`, with keys such as `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.

### 41. How does login work?

The backend searches the user by username or email. It compares the entered password with the stored password hash.

### 42. Why store password hash instead of password?

A hash protects the original password. If someone reads the database, they do not see plain passwords.

### 43. How does the app know a user is logged in?

Flask stores the logged-in user's id in the session.

### 44. How does the app protect pages from anonymous users?

Routes such as dashboard, expenses, income, and reports use a `login_required` wrapper. If no user is logged in, the app redirects to login.

## Testing Questions

### 45. Did you test the project?

Yes. The project includes automated tests with pytest.

### 46. What do the tests check?

Tests check validation, balance calculation, route behavior, config loading, stored procedure result handling, and required SQL artifacts.

### 47. How do you run tests?

```powershell
.\.venv\Scripts\python.exe -m pytest
```

### 48. Did you test with MySQL?

Yes. The schema and sample data were loaded into MySQL, and the sample monthly report returned the expected balance.

## Security and Validation Questions

### 49. What validations did you add?

The app validates registration fields, positive money amounts, and date format.

### 50. Can users enter negative expenses?

No. The backend rejects non-positive amounts, and the database also has check constraints.

### 51. How do you prevent one user from seeing another user's records?

Queries filter records by `user_id` from the current session.

### 52. What security improvement would you add next?

I would add CSRF protection for forms and password reset through email.

## Report Questions

### 53. How is the monthly report generated?

The app calls `sp_monthly_report(user_id, year, month)`. The procedure returns the monthly summary, expense category summary, and income category summary.

### 54. What is the formula for balance?

```text
Balance = Total Income - Total Expense
```

### 55. What data appears in category-wise reports?

The report shows each category name, transaction count, and total amount for the selected month.

## Practical Demo Questions

### 56. How do you run the project?

Activate the virtual environment, make sure MySQL is running, load the schema and sample data, configure `.env`, and run:

```powershell
python app.py
```

### 57. Which URL opens the app?

```text
http://127.0.0.1:5000
```

### 58. Which SQL files should be loaded?

Load `database/schema.sql` first, then `database/sample_data.sql`.

### 59. Where can the evaluator see SQL query examples?

The file `database/queries.sql` contains example queries.

### 60. Where is the ER diagram?

The ER diagram is in `docs/ER_DIAGRAM.md`.

## Limitations and Future Scope

### 61. What are the limitations of this project?

The project does not include charts, PDF export, budget alerts, or password reset.

### 62. What features can you add in the future?

I can add budget limits, graphs, CSV/PDF export, recurring transactions, and yearly reports.

### 63. Can this project become a larger app?

Yes. It can become a personal finance dashboard with budgets, reminders, analytics, and mobile support.

## Short Answers to Remember

- Main formula: `balance = income - expense`
- Main relationship: one user has many income and expense records
- Main DBMS features: normalization, joins, views, triggers, stored procedures
- Main security feature: password hashing
- Main report procedure: `sp_monthly_report`
- Main trigger purpose: recalculate monthly balance automatically

