"""
Path: config_manager/sqlite_loader.py
Description: This module contains the SQLiteConfigLoader class which is used to load and save
configuration data from/to a SQLite database.
"""

import sqlite3
from typing import Dict, Any, Optional
from .base_loader import BaseConfigLoader
import uuid


class SQLiteConfigLoader(BaseConfigLoader):
    def __init__(
        self, sqlite_location: str, app_name: str, app_id: Optional[str] = None
    ):
        """
        Initialize the SQLiteConfigLoader.
        :param sqlite_location: Path to the SQLite database.
        :param app_name: Name of the application.
        :param app_id: Unique identifier for the application.
        """
        self.sqlite_location = sqlite_location
        self.app_name = app_name
        self.app_id = app_id or str(uuid.uuid4())
        self.initialize_database()

    def initialize_database(self) -> None:
        """
        Initialize the SQLite database.
        :return: None
        """
        connection = sqlite3.connect(self.sqlite_location)
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS applications (
                    app_id TEXT PRIMARY KEY,
                    app_name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_id TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (app_id, key),
                    FOREIGN KEY (app_id) REFERENCES applications(app_id) ON DELETE CASCADE
                );
            """
            )
            connection.commit()
        except Exception as e:
            print("Error initializing database:", e)
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    def initialize_application(self) -> None:
        """
        Initialize the application in the database.
        :return: None
        """
        connection = sqlite3.connect(self.sqlite_location)
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO applications (app_id, app_name)
                VALUES (?, ?);
            """,
                (self.app_id, self.app_name),
            )
            connection.commit()
        except Exception as e:
            print("Error initializing application:", e)
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    def load(self) -> Dict[str, Any]:
        """
        Load configuration data from the SQLite database.
        :return: None
        """
        config = {}
        connection = sqlite3.connect(self.sqlite_location)
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT key, value FROM config
                WHERE app_id = ?;
            """,
                (self.app_id,),
            )
            rows = cursor.fetchall()
            for key, value in rows:
                config[key] = value
        except Exception as e:
            print("Error loading configuration:", e)
            raise
        finally:
            cursor.close()
            connection.close()
        return config

    def save(self, config: Dict[str, Any]) -> None:
        """
        Save configuration data to the SQLite database.
        :param config: A dict containing configuration data.
        :return: None
        """
        connection = sqlite3.connect(self.sqlite_location)
        cursor = connection.cursor()
        try:
            # Ensure the application exists
            self.initialize_application()

            for key, value in config.items():
                cursor.execute(
                    """
                    INSERT INTO config (app_id, key, value)
                    VALUES (?, ?, ?)
                    ON CONFLICT(app_id, key) DO UPDATE SET
                        value = excluded.value,
                        updated_at = CURRENT_TIMESTAMP;
                """,
                    (self.app_id, key, value),
                )
            connection.commit()
        except Exception as e:
            print("Error saving configuration:", e)
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()
