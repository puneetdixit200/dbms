# Project Understanding and Pitch Guide

Use this document to explain the project in class, during a viva, or in a mini-project review.

## One-Line Pitch

Personal Expense Tracker is a DBMS-based web app that lets a user record income and expenses, organize them by category, and view monthly balance reports generated from MySQL tables, joins, views, triggers, and stored procedures.

## Simple Explanation

This project solves a common personal finance problem: many students and working people do not know where their money goes each month. The app gives them one place to record income, expenses, categories, dates, payment methods, and monthly reports.

The frontend uses HTML, CSS, and JavaScript. The backend uses Python Flask. MySQL stores all records. The database does important work too. It keeps the data normalized, connects related tables using foreign keys, generates category summaries through views, and updates monthly balances through triggers.

## Problem Statement

Users need a simple system to track daily expenses and income. A spreadsheet can store this data, but it can repeat information, create update errors, and make reports harder to manage. This project uses DBMS concepts to store financial data in structured tables and calculate monthly summaries with better consistency.

## Objectives

- Let users register and log in.
- Let users add, edit, and delete expense records.
- Let users add, edit, and delete income records.
- Store income and expense categories separately.
- Generate monthly income, expense, and balance reports.
- Demonstrate DBMS concepts through normalized tables, joins, triggers, views, and stored procedures.

## Target Users

- Students tracking pocket money, rent, food, transport, and study costs.
- Working users tracking salary, freelance income, rent, bills, and daily spending.
- Beginners learning how a web app connects with a relational database.

## Main Features

### User Login and Registration

The user creates an account with username, email, and password. The app stores the password as a hash, not plain text.

### Expense Management

The user can add expense records with amount, date, category, payment method, and description. The user can update or delete any expense later.

### Income Tracking

The user can record salary, freelance income, gifts, bank interest, or any other income source.

### Categories

The app stores categories in a separate table. Each user gets separate categories, so one user's categories do not affect another user's records.

### Monthly Reports

The reports page shows total income, total expense, and balance for a selected month. It also shows income and expense totals grouped by category.

## DBMS Concepts Used

### Primary Keys

Each main table has a primary key. For example, `users.id`, `categories.id`, `expenses.id`, and `incomes.id`.

### Foreign Keys

Foreign keys connect records:

- `categories.user_id` links categories to users.
- `expenses.user_id` links expenses to users.
- `expenses.category_id` links expenses to categories.
- `incomes.user_id` links income records to users.
- `incomes.category_id` links income records to categories.

### Normalization

The database keeps users, categories, expenses, incomes, and monthly balances in separate tables. This reduces duplicate data and prevents category names from being repeated inside every transaction row.

### Joins

The app uses joins to show transaction records with category names. For example, expense records join with categories using `expenses.category_id = categories.id`.

### Views

Views prepare report-friendly data:

- `v_monthly_financial_summary`
- `v_expense_category_summary`
- `v_income_category_summary`

### Triggers

Triggers update monthly balances after insert, update, or delete operations on income and expense tables. This keeps the report table current.

### Stored Procedures

Stored procedures handle repeated database actions such as adding, updating, deleting, and reporting records.

## Why This Project Is Useful

The project shows both application development and database design. It does not only store data. It shows how a backend can call database procedures, how triggers can maintain summaries, and how normalized tables support clean reports.

## Demo Flow

Use this order during presentation:

1. Open the login page.
2. Log in with the sample user:

```text
Email: student@example.com
Password: sample123
```

3. Open the dashboard and show monthly income, expenses, and balance.
4. Go to Expenses and add a new expense.
5. Edit the new expense.
6. Delete the new expense.
7. Go to Income and add an income record.
8. Go to Reports and show category-wise monthly totals.
9. Open `database/schema.sql` and point out tables, triggers, views, and stored procedures.

## Two-Minute Presentation Script

Good morning. My mini project is Personal Expense Tracker Using DBMS. The purpose of this project is to help a user record income and expenses and view monthly balance reports.

The project uses HTML, CSS, and JavaScript for the frontend. The backend uses Python Flask, and the database is MySQL. A user can register, log in, add expenses, edit or delete them, record income, manage categories, and view monthly reports.

The important DBMS part is the database design. I created separate tables for users, categories, expenses, incomes, and monthly balances. This keeps the database normalized and avoids duplicate data. The project uses foreign keys to connect tables, joins to display category names with transactions, views to generate category summaries, triggers to update monthly balance after every insert, update, or delete, and stored procedures for common operations.

For example, when a user adds an expense, the backend calls a stored procedure. After the expense is inserted, a trigger recalculates the monthly balance. The report page then reads the updated summary.

This project helped me understand how a web application and DBMS work together in a practical system.

## Five-Minute Presentation Structure

### 1. Introduction

Start with the problem: people often spend money daily but do not track it properly. Explain that the app gives users a simple way to record and review finances.

### 2. Technology Stack

Mention:

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: MySQL

### 3. Modules

Explain authentication, expense management, income tracking, categories, and reports.

### 4. Database Design

Show the ER diagram. Explain each table and the relationships.

### 5. DBMS Features

Point out:

- Joins for transaction display
- Views for summaries
- Triggers for automatic balance updates
- Stored procedures for add, update, delete, and report operations
- Normalization up to 3NF

### 6. Live Demo

Show login, dashboard, expense entry, income entry, and monthly report.

### 7. Conclusion

End with one sentence: the project connects a simple finance use case with core DBMS concepts in a working web application.

## Slide Outline

1. Title
2. Problem Statement
3. Objectives
4. Technology Stack
5. System Modules
6. ER Diagram
7. Tables and Relationships
8. DBMS Concepts Used
9. Demo Screens
10. Testing and Future Scope

## Strengths to Mention

- The database uses foreign keys, not loose unrelated tables.
- The schema separates income and expenses.
- The report logic uses MySQL views and stored procedures.
- Triggers keep monthly balances updated.
- Passwords use hashing.
- The project includes sample data and beginner setup docs.

## Limitations

- The app does not include charts yet.
- The app does not export reports to PDF or Excel.
- The app runs as a local development project, not a production deployment.
- The app has simple session-based authentication.

## Future Scope

- Add budget limits by category.
- Add charts for monthly and yearly trends.
- Add CSV or PDF report export.
- Add recurring income and expense records.
- Add a mobile-friendly dashboard with graphs.
- Add password reset.

## Files to Show During Review

- `database/schema.sql`: tables, views, triggers, stored procedures
- `database/sample_data.sql`: demo data
- `database/queries.sql`: query examples
- `docs/ER_DIAGRAM.md`: ER diagram
- `docs/NORMALIZATION.md`: normalization explanation
- `docs/PROJECT_REPORT.md`: full project report
- `docs/RUN_GUIDE.md`: setup steps

