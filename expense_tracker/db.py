from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator


class DatabaseError(RuntimeError):
    """Raised when the MySQL connection cannot be created or used."""


class Database:
    def __init__(self, config: dict[str, Any]):
        self.host = config["DB_HOST"]
        self.port = config["DB_PORT"]
        self.user = config["DB_USER"]
        self.password = config["DB_PASSWORD"]
        self.database = config["DB_NAME"]

    def connect(self):
        try:
            import mysql.connector
        except ModuleNotFoundError as exc:
            raise DatabaseError(
                "mysql-connector-python is not installed. Run: pip install -r requirements.txt"
            ) from exc

        try:
            return mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=False,
            )
        except Exception as exc:  # mysql.connector.Error is unavailable until imported.
            raise DatabaseError(
                "Could not connect to MySQL. Check .env values and load database/schema.sql."
            ) from exc

    @contextmanager
    def transaction(self, dictionary: bool = True) -> Iterator[Any]:
        connection = self.connect()
        cursor = connection.cursor(dictionary=dictionary)
        try:
            yield cursor
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

