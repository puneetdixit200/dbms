USE personal_expense_tracker;

-- 1. Login lookup used by the backend.
SELECT id, username, email, password_hash
FROM users
WHERE username = 'student' OR email = 'student@example.com'
LIMIT 1;

-- 2. Expense list with INNER JOIN between expenses and categories.
SELECT
    e.id,
    e.expense_date,
    c.name AS category,
    e.description,
    e.payment_method,
    e.amount
FROM expenses e
INNER JOIN categories c ON c.id = e.category_id
WHERE e.user_id = 1
ORDER BY e.expense_date DESC;

-- 3. Income list with INNER JOIN between incomes and categories.
SELECT
    i.id,
    i.income_date,
    c.name AS category,
    i.source,
    i.amount
FROM incomes i
INNER JOIN categories c ON c.id = i.category_id
WHERE i.user_id = 1
ORDER BY i.income_date DESC;

-- 4. Monthly income, expense, and balance from the trigger-maintained table.
SELECT year_no, month_no, total_income, total_expense, balance
FROM monthly_balances
WHERE user_id = 1 AND year_no = 2026 AND month_no = 5;

-- 5. Category-wise expense report from a view.
SELECT category_name, transaction_count, total_amount
FROM v_expense_category_summary
WHERE user_id = 1 AND year_no = 2026 AND month_no = 5
ORDER BY total_amount DESC;

-- 6. Stored procedure call used by the reports page.
CALL sp_monthly_report(1, 2026, 5);

-- 7. Insert through stored procedure. The expense trigger recalculates monthly balance.
CALL sp_add_expense(1, 1, 250.00, '2026-05-19', 'Tea and snacks', 'Cash');

-- 8. Delete through stored procedure. The delete trigger recalculates monthly balance.
CALL sp_delete_expense(8, 1);

