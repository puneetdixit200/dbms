# Personal Expense Tracker Using DBMS

A DBMS mini project built with HTML/CSS/JavaScript, Python Flask, and MySQL.

## Features

- User registration and login with hashed passwords
- Add, edit, and delete expenses
- Income tracking
- User-specific income and expense categories
- Monthly reports with income, expense, and balance calculation
- MySQL joins, views, triggers, and stored procedures
- Sample data and project documentation

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: MySQL 8+

## Project Structure

```text
.
|-- app.py
|-- expense_tracker/
|   |-- config.py
|   |-- db.py
|   |-- finance.py
|   |-- repositories.py
|   |-- routes.py
|   `-- validators.py
|-- templates/
|-- static/
|-- database/
|   |-- schema.sql
|   |-- sample_data.sql
|   `-- queries.sql
|-- docs/
|-- tests/
|-- requirements.txt
`-- .env.example
```

## Quick Start

1. Install Python 3.11+ and MySQL 8+.
2. Open PowerShell in this project folder.
3. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

5. Create the MySQL database and tables:

```powershell
mysql -u root -p -e "source database/schema.sql"
mysql -u root -p -e "source database/sample_data.sql"
```

6. Create a `.env` file:

```powershell
Copy-Item .env.example .env
```

7. Edit `.env` and set your MySQL password.
8. Run the app:

```powershell
python app.py
```

9. Open `http://127.0.0.1:5000`.

Sample login after loading sample data:

- Email: `student@example.com`
- Password: `sample123`

## Tests

```powershell
pytest
```

The included tests do not require a running MySQL server. Full manual testing of add/edit/delete/report flows requires loading `database/schema.sql` and `database/sample_data.sql` into MySQL.

## Documentation

- [Noob Run Guide](docs/RUN_GUIDE.md)
- [Project Report](docs/PROJECT_REPORT.md)
- [ER Diagram](docs/ER_DIAGRAM.md)
- [Normalization](docs/NORMALIZATION.md)
- [Project Understanding and Pitch Guide](docs/PITCH_GUIDE.md)
- [Project Viva and Q&A](docs/VIVA_QA.md)
