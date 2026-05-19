CREATE DATABASE IF NOT EXISTS personal_expense_tracker;
USE personal_expense_tracker;

SET FOREIGN_KEY_CHECKS = 0;
DROP TRIGGER IF EXISTS trg_expenses_after_insert;
DROP TRIGGER IF EXISTS trg_expenses_after_update;
DROP TRIGGER IF EXISTS trg_expenses_after_delete;
DROP TRIGGER IF EXISTS trg_incomes_after_insert;
DROP TRIGGER IF EXISTS trg_incomes_after_update;
DROP TRIGGER IF EXISTS trg_incomes_after_delete;
DROP PROCEDURE IF EXISTS sp_recalculate_monthly_balance;
DROP PROCEDURE IF EXISTS sp_add_expense;
DROP PROCEDURE IF EXISTS sp_update_expense;
DROP PROCEDURE IF EXISTS sp_delete_expense;
DROP PROCEDURE IF EXISTS sp_add_income;
DROP PROCEDURE IF EXISTS sp_update_income;
DROP PROCEDURE IF EXISTS sp_delete_income;
DROP PROCEDURE IF EXISTS sp_monthly_report;
DROP VIEW IF EXISTS v_monthly_financial_summary;
DROP VIEW IF EXISTS v_expense_category_summary;
DROP VIEW IF EXISTS v_income_category_summary;
DROP TABLE IF EXISTS monthly_balances;
DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS incomes;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_users_username_len CHECK (CHAR_LENGTH(username) >= 3)
) ENGINE = InnoDB;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(80) NOT NULL,
    type ENUM('expense', 'income') NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_categories_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT uq_categories_user_type_name UNIQUE (user_id, type, name)
) ENGINE = InnoDB;

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    expense_date DATE NOT NULL,
    description VARCHAR(255),
    payment_method VARCHAR(50) DEFAULT 'Cash',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_expenses_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_expenses_category
        FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE RESTRICT,
    CONSTRAINT chk_expenses_amount CHECK (amount > 0),
    INDEX idx_expenses_user_date (user_id, expense_date),
    INDEX idx_expenses_category (category_id)
) ENGINE = InnoDB;

CREATE TABLE incomes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    income_date DATE NOT NULL,
    source VARCHAR(100),
    notes VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_incomes_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_incomes_category
        FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE RESTRICT,
    CONSTRAINT chk_incomes_amount CHECK (amount > 0),
    INDEX idx_incomes_user_date (user_id, income_date),
    INDEX idx_incomes_category (category_id)
) ENGINE = InnoDB;

CREATE TABLE monthly_balances (
    user_id INT NOT NULL,
    year_no INT NOT NULL,
    month_no INT NOT NULL,
    total_income DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    total_expense DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    balance DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, year_no, month_no),
    CONSTRAINT fk_monthly_balances_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT chk_monthly_balances_month CHECK (month_no BETWEEN 1 AND 12)
) ENGINE = InnoDB;

CREATE VIEW v_monthly_financial_summary AS
SELECT
    mb.user_id,
    u.username,
    mb.year_no,
    mb.month_no,
    mb.total_income,
    mb.total_expense,
    mb.balance,
    mb.updated_at
FROM monthly_balances mb
INNER JOIN users u ON u.id = mb.user_id;

CREATE VIEW v_expense_category_summary AS
SELECT
    e.user_id,
    YEAR(e.expense_date) AS year_no,
    MONTH(e.expense_date) AS month_no,
    c.id AS category_id,
    c.name AS category_name,
    COUNT(*) AS transaction_count,
    SUM(e.amount) AS total_amount
FROM expenses e
INNER JOIN categories c ON c.id = e.category_id
GROUP BY e.user_id, YEAR(e.expense_date), MONTH(e.expense_date), c.id, c.name;

CREATE VIEW v_income_category_summary AS
SELECT
    i.user_id,
    YEAR(i.income_date) AS year_no,
    MONTH(i.income_date) AS month_no,
    c.id AS category_id,
    c.name AS category_name,
    COUNT(*) AS transaction_count,
    SUM(i.amount) AS total_amount
FROM incomes i
INNER JOIN categories c ON c.id = i.category_id
GROUP BY i.user_id, YEAR(i.income_date), MONTH(i.income_date), c.id, c.name;

DELIMITER //

CREATE PROCEDURE sp_recalculate_monthly_balance(
    IN p_user_id INT,
    IN p_year INT,
    IN p_month INT
)
BEGIN
    DECLARE v_income DECIMAL(12, 2) DEFAULT 0.00;
    DECLARE v_expense DECIMAL(12, 2) DEFAULT 0.00;

    SELECT COALESCE(SUM(amount), 0.00)
    INTO v_income
    FROM incomes
    WHERE user_id = p_user_id
      AND YEAR(income_date) = p_year
      AND MONTH(income_date) = p_month;

    SELECT COALESCE(SUM(amount), 0.00)
    INTO v_expense
    FROM expenses
    WHERE user_id = p_user_id
      AND YEAR(expense_date) = p_year
      AND MONTH(expense_date) = p_month;

    INSERT INTO monthly_balances (
        user_id,
        year_no,
        month_no,
        total_income,
        total_expense,
        balance
    )
    VALUES (
        p_user_id,
        p_year,
        p_month,
        v_income,
        v_expense,
        v_income - v_expense
    )
    ON DUPLICATE KEY UPDATE
        total_income = VALUES(total_income),
        total_expense = VALUES(total_expense),
        balance = VALUES(balance),
        updated_at = CURRENT_TIMESTAMP;
END//

CREATE PROCEDURE sp_add_expense(
    IN p_user_id INT,
    IN p_category_id INT,
    IN p_amount DECIMAL(10, 2),
    IN p_expense_date DATE,
    IN p_description VARCHAR(255),
    IN p_payment_method VARCHAR(50)
)
BEGIN
    INSERT INTO expenses (user_id, category_id, amount, expense_date, description, payment_method)
    VALUES (p_user_id, p_category_id, p_amount, p_expense_date, p_description, p_payment_method);
END//

CREATE PROCEDURE sp_update_expense(
    IN p_expense_id INT,
    IN p_user_id INT,
    IN p_category_id INT,
    IN p_amount DECIMAL(10, 2),
    IN p_expense_date DATE,
    IN p_description VARCHAR(255),
    IN p_payment_method VARCHAR(50)
)
BEGIN
    UPDATE expenses
    SET category_id = p_category_id,
        amount = p_amount,
        expense_date = p_expense_date,
        description = p_description,
        payment_method = p_payment_method
    WHERE id = p_expense_id
      AND user_id = p_user_id;
END//

CREATE PROCEDURE sp_delete_expense(
    IN p_expense_id INT,
    IN p_user_id INT
)
BEGIN
    DELETE FROM expenses
    WHERE id = p_expense_id
      AND user_id = p_user_id;
END//

CREATE PROCEDURE sp_add_income(
    IN p_user_id INT,
    IN p_category_id INT,
    IN p_amount DECIMAL(10, 2),
    IN p_income_date DATE,
    IN p_source VARCHAR(100),
    IN p_notes VARCHAR(255)
)
BEGIN
    INSERT INTO incomes (user_id, category_id, amount, income_date, source, notes)
    VALUES (p_user_id, p_category_id, p_amount, p_income_date, p_source, p_notes);
END//

CREATE PROCEDURE sp_update_income(
    IN p_income_id INT,
    IN p_user_id INT,
    IN p_category_id INT,
    IN p_amount DECIMAL(10, 2),
    IN p_income_date DATE,
    IN p_source VARCHAR(100),
    IN p_notes VARCHAR(255)
)
BEGIN
    UPDATE incomes
    SET category_id = p_category_id,
        amount = p_amount,
        income_date = p_income_date,
        source = p_source,
        notes = p_notes
    WHERE id = p_income_id
      AND user_id = p_user_id;
END//

CREATE PROCEDURE sp_delete_income(
    IN p_income_id INT,
    IN p_user_id INT
)
BEGIN
    DELETE FROM incomes
    WHERE id = p_income_id
      AND user_id = p_user_id;
END//

CREATE PROCEDURE sp_monthly_report(
    IN p_user_id INT,
    IN p_year INT,
    IN p_month INT
)
BEGIN
    SELECT
        year_no,
        month_no,
        total_income,
        total_expense,
        balance
    FROM monthly_balances
    WHERE user_id = p_user_id
      AND year_no = p_year
      AND month_no = p_month;

    SELECT
        category_id,
        category_name,
        transaction_count,
        total_amount
    FROM v_expense_category_summary
    WHERE user_id = p_user_id
      AND year_no = p_year
      AND month_no = p_month
    ORDER BY total_amount DESC;

    SELECT
        category_id,
        category_name,
        transaction_count,
        total_amount
    FROM v_income_category_summary
    WHERE user_id = p_user_id
      AND year_no = p_year
      AND month_no = p_month
    ORDER BY total_amount DESC;
END//

CREATE TRIGGER trg_expenses_after_insert
AFTER INSERT ON expenses
FOR EACH ROW
BEGIN
    CALL sp_recalculate_monthly_balance(NEW.user_id, YEAR(NEW.expense_date), MONTH(NEW.expense_date));
END//

CREATE TRIGGER trg_expenses_after_update
AFTER UPDATE ON expenses
FOR EACH ROW
BEGIN
    IF OLD.user_id <> NEW.user_id
       OR YEAR(OLD.expense_date) <> YEAR(NEW.expense_date)
       OR MONTH(OLD.expense_date) <> MONTH(NEW.expense_date) THEN
        CALL sp_recalculate_monthly_balance(OLD.user_id, YEAR(OLD.expense_date), MONTH(OLD.expense_date));
    END IF;
    CALL sp_recalculate_monthly_balance(NEW.user_id, YEAR(NEW.expense_date), MONTH(NEW.expense_date));
END//

CREATE TRIGGER trg_expenses_after_delete
AFTER DELETE ON expenses
FOR EACH ROW
BEGIN
    CALL sp_recalculate_monthly_balance(OLD.user_id, YEAR(OLD.expense_date), MONTH(OLD.expense_date));
END//

CREATE TRIGGER trg_incomes_after_insert
AFTER INSERT ON incomes
FOR EACH ROW
BEGIN
    CALL sp_recalculate_monthly_balance(NEW.user_id, YEAR(NEW.income_date), MONTH(NEW.income_date));
END//

CREATE TRIGGER trg_incomes_after_update
AFTER UPDATE ON incomes
FOR EACH ROW
BEGIN
    IF OLD.user_id <> NEW.user_id
       OR YEAR(OLD.income_date) <> YEAR(NEW.income_date)
       OR MONTH(OLD.income_date) <> MONTH(NEW.income_date) THEN
        CALL sp_recalculate_monthly_balance(OLD.user_id, YEAR(OLD.income_date), MONTH(OLD.income_date));
    END IF;
    CALL sp_recalculate_monthly_balance(NEW.user_id, YEAR(NEW.income_date), MONTH(NEW.income_date));
END//

CREATE TRIGGER trg_incomes_after_delete
AFTER DELETE ON incomes
FOR EACH ROW
BEGIN
    CALL sp_recalculate_monthly_balance(OLD.user_id, YEAR(OLD.income_date), MONTH(OLD.income_date));
END//

DELIMITER ;

