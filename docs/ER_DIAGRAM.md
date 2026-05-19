# ER Diagram

```mermaid
erDiagram
    USERS ||--o{ CATEGORIES : owns
    USERS ||--o{ EXPENSES : records
    USERS ||--o{ INCOMES : records
    USERS ||--o{ MONTHLY_BALANCES : has
    CATEGORIES ||--o{ EXPENSES : classifies
    CATEGORIES ||--o{ INCOMES : classifies

    USERS {
        int id PK
        varchar username UK
        varchar email UK
        varchar password_hash
        timestamp created_at
    }

    CATEGORIES {
        int id PK
        int user_id FK
        varchar name
        enum type
        timestamp created_at
    }

    EXPENSES {
        int id PK
        int user_id FK
        int category_id FK
        decimal amount
        date expense_date
        varchar description
        varchar payment_method
        timestamp created_at
        timestamp updated_at
    }

    INCOMES {
        int id PK
        int user_id FK
        int category_id FK
        decimal amount
        date income_date
        varchar source
        varchar notes
        timestamp created_at
        timestamp updated_at
    }

    MONTHLY_BALANCES {
        int user_id PK, FK
        int year_no PK
        int month_no PK
        decimal total_income
        decimal total_expense
        decimal balance
        timestamp updated_at
    }
```

## Relationship Notes

- One user can have many categories.
- One user can have many expenses and many income records.
- One category can classify many expenses or income records.
- One user has one monthly balance row per year and month.
- `monthly_balances` is maintained automatically by triggers after insert, update, and delete operations on `expenses` and `incomes`.

