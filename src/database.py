"""Database module for SQLite connection and queries."""

import sqlite3
from functools import lru_cache
from pathlib import Path
from typing import Any

import chainlit as cl
import pandas as pd

from config import get_settings
from src.schemas import DBQueryError, DBQuerySuccess

TABLE_FILES = {
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
}


class Database:
    """SQLite database wrapper with per-query connections."""

    def __init__(self, path: Path | str):
        """
        Initialize database wrapper.

        Args:
            path: Path to the SQLite database file.

        """
        self.path = Path(path)

    def _get_connection(self) -> sqlite3.Connection:
        """Create a new database connection."""
        conn = sqlite3.connect(str(self.path))
        conn.row_factory = sqlite3.Row
        return conn

    def fetch_all(self, query: str, params: list[Any] | None = None) -> list[dict]:
        """
        Execute query and fetch all results as dictionaries.

        Args:
            query: SQL query string.
            params: Optional list of query parameters.

        Returns:
            List of result rows as dictionaries.

        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def fetch_one(self, query: str, params: list[Any] | None = None) -> dict | None:
        """
        Execute query and fetch single result as dictionary.

        Args:
            query: SQL query string.
            params: Optional list of query parameters.

        Returns:
            Single result row as dictionary, or None if no results.

        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            row = cursor.fetchone()
            return dict(row) if row else None

    def ensure_tables_exist(self, data_dir: Path | None = None) -> None:
        """
        Ensure all expected tables exist, importing from CSVs if needed.

        Args:
            data_dir: Directory containing source CSV files. Defaults to settings.data_dir.

        """
        if data_dir is None:
            data_dir = get_settings().data_dir

        expected_tables = set(TABLE_FILES.keys())

        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'",
            )
            existing_tables = {row["name"] for row in cursor.fetchall()}
            missing_tables = expected_tables - existing_tables

            if not missing_tables:
                return

            if existing_tables:
                print(
                    f"Importing {len(missing_tables)} missing table(s): "
                    f"{', '.join(sorted(missing_tables))}",
                )
            else:
                print(f"Initializing database with {len(expected_tables)} tables...")

            for table in missing_tables:
                filename = TABLE_FILES[table]
                file_path = data_dir / filename
                if not file_path.exists():
                    print(f"   Warning: File {filename} not found.")
                    continue

                print(f"   -> Importing {table}...")
                df = pd.read_csv(file_path)

                for col in df.columns:
                    if "timestamp" in col or "date" in col:
                        df[col] = pd.to_datetime(df[col], errors="coerce")

                df.to_sql(table, conn, if_exists="replace", index=False)

            print("Database ready.")


@lru_cache
def get_database() -> Database:
    """
    Get database instance using settings path.

    Ensures all expected tables exist before returning.

    Returns:
        Database instance connected to marketplace_data.db.

    """
    settings = get_settings()
    db = Database(settings.database_path)
    db.ensure_tables_exist(settings.data_dir)
    return db


@cl.step(name="Execute Query", type="tool")
async def execute_query(query: str, params: list[Any] | None = None) -> dict[str, Any]:
    """Execute a SQL query against the marketplace database."""
    db = get_database()
    try:
        rows = db.fetch_all(query, params)
        return DBQuerySuccess(rows=rows, count=len(rows)).model_dump()
    except Exception as e:
        return DBQueryError(error=str(e)).model_dump()
