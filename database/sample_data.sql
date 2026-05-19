USE personal_expense_tracker;

INSERT INTO users (id, username, email, password_hash)
VALUES
(
    1,
    'student',
    'student@example.com',
    'scrypt:32768:8:1$77wpgvt2N3kv01W2$be42597425fa288069ba6c1f97f17e6f76a7666953000bb1457efb4f6abcba39d17e225830d5874fd10d855acf82fe55ddb5ede98ea3eb4cef66eeff33d2502b'
);

INSERT INTO categories (id, user_id, name, type)
VALUES
(1, 1, 'Food', 'expense'),
(2, 1, 'Transport', 'expense'),
(3, 1, 'Rent', 'expense'),
(4, 1, 'Utilities', 'expense'),
(5, 1, 'Education', 'expense'),
(6, 1, 'Entertainment', 'expense'),
(7, 1, 'Salary', 'income'),
(8, 1, 'Freelance', 'income'),
(9, 1, 'Gift', 'income'),
(10, 1, 'Interest', 'income');

INSERT INTO incomes (user_id, category_id, amount, income_date, source, notes)
VALUES
(1, 7, 45000.00, '2026-05-01', 'Monthly salary', 'May salary'),
(1, 8, 6500.00, '2026-05-09', 'Website project', 'Freelance client'),
(1, 10, 450.00, '2026-05-15', 'Savings account', 'Bank interest'),
(1, 7, 45000.00, '2026-04-01', 'Monthly salary', 'April salary');

INSERT INTO expenses (user_id, category_id, amount, expense_date, description, payment_method)
VALUES
(1, 3, 12000.00, '2026-05-02', 'Hostel rent', 'UPI'),
(1, 1, 2450.00, '2026-05-05', 'Groceries and snacks', 'Card'),
(1, 2, 900.00, '2026-05-08', 'Bus pass', 'Cash'),
(1, 4, 1800.00, '2026-05-12', 'Electricity bill', 'UPI'),
(1, 5, 3200.00, '2026-05-16', 'Course material', 'Card'),
(1, 6, 750.00, '2026-05-18', 'Movie', 'UPI'),
(1, 1, 2100.00, '2026-04-06', 'Groceries', 'Card');

