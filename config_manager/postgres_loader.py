"""
Package: config_manager
Module: postgres_loader
This module contains the PostgresConfigLoader class that is used to load and save configuration data from PostgreSQL database.
"""

import uuid
from typing import Any, Dict, Optional

import psycopg2

from .base_loader import BaseConfigLoader


class PostgresConfigLoader(BaseConfigLoader):
    """
    Configuration loader for PostgreSQL database.
    """

    def __init__(
        self,
        postgres_uri: str,
        app_name: str,
        app_id: Optional[str] = None,
        postgres_table: str = "config",
        applications_table: str = "applications",
    ):
        """
        Initialize the PostgresConfigLoader.
        :param postgres_uri: URI for the PostgreSQL database.
        :param app_name: Name of the application.
        :param app_id: Unique identifier for the application.
        :param postgres_table: Name of the table to store configuration data.
        :param applications_table: Name of the table to store application data.
        """
        self.postgres_uri = postgres_uri
        self.postgres_table = postgres_table
        self.applications_table = applications_table
        self.app_name = app_name
        self.app_id = app_id or str(uuid.uuid4())

    def initialize_application(self) -> None:
        """
        Initialize a new application in the database.
        :return: None
        """
        connection = psycopg2.connect(self.postgres_uri)
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                INSERT INTO {self.applications_table} (app_id, app_name)
                VALUES (%s, %s)
                ON CONFLICT (app_name) DO NOTHING;
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
        Load configuration data from the database.
        :return: Dict containing configuration data.
        """
        config = {}
        connection = psycopg2.connect(self.postgres_uri)
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                SELECT key, value FROM {self.postgres_table}
                WHERE app_id = %s;
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
        Save configuration data to the database.
        :param config: A dict containing configuration data.
        :return: None
        """
        connection = psycopg2.connect(self.postgres_uri)
        cursor = connection.cursor()
        try:
            # Ensure the application exists
            self.initialize_application()

            for key, value in config.items():
                cursor.execute(
                    f"""
                    INSERT INTO {self.postgres_table} (app_id, key, value)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (app_id, key) DO UPDATE
                    SET value = EXCLUDED.value,
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

    def create_schema(self) -> None:
        """
        Create the necessary tables in the database.
        :return: None
        """
        sql = f"""
CREATE TABLE IF NOT EXISTS applications (
    app_id UUID PRIMARY KEY,
    app_name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS config (
    id SERIAL PRIMARY KEY,
    app_id UUID REFERENCES applications(app_id) ON DELETE CASCADE,
    key TEXT NOT NULL,
    value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (app_id, key)
);
                """
        connection = psycopg2.connect(self.postgres_uri)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            print("Error creating schema:", e)
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()
