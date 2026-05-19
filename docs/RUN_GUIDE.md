# Step-by-Step Run Guide

This guide is written for a beginner running the project on Windows.

## 1. Install Required Software

Install these first:

- Python 3.11 or newer
- MySQL Server 8 or newer
- Git
- Any code editor, such as VS Code

During MySQL installation, remember the password you set for the `root` user.

## 2. Download the Project

Open PowerShell and run:

```powershell
git clone https://github.com/puneetdixit200/dbms.git
cd dbms
```

If you already have the folder, just open PowerShell inside the project folder.

## 3. Create Python Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Install Python Packages

```powershell
pip install -r requirements.txt
```

## 5. Create MySQL Database

Make sure MySQL Server is running. Then run:

```powershell
mysql -u root -p -e "source database/schema.sql"
```

Enter your MySQL root password when asked.

## 6. Add Sample Data

```powershell
mysql -u root -p -e "source database/sample_data.sql"
```

This adds a demo user, categories, income records, and expense records.

## 7. Configure Database Password

Create your local `.env` file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and edit:

```text
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=personal_expense_tracker
```

Keep `DB_HOST=127.0.0.1` and `DB_PORT=3306` unless your MySQL setup is different.

## 8. Run the Project

```powershell
python app.py
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

## 9. Demo Login

Use this account after loading sample data:

```text
Email: student@example.com
Password: sample123
```

You can also register a new account from the Register page.

## 10. How to Use the App

1. Register or log in.
2. Go to Expenses and add expense records.
3. Use Save to edit an expense.
4. Use Delete to remove an expense.
5. Go to Income and add income records.
6. Go to Reports and select year/month.
7. Check total income, total expenses, and balance.

## 11. Run Tests

```powershell
pytest
```

These tests check validation, balance calculation, Flask page loading, and required SQL artifacts.

## 12. Common Errors

`mysql is not recognized`

MySQL is not added to PATH. Use MySQL Workbench to run the SQL files, or add the MySQL `bin` folder to PATH.

`Could not connect to MySQL`

Check that MySQL Server is running and `.env` has the correct `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.

`Access denied for user root`

Your MySQL password is wrong, or your MySQL user is not `root`.

`ModuleNotFoundError`

Activate the virtual environment and run `pip install -r requirements.txt` again.
