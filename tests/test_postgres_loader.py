from unittest.mock import MagicMock, call, patch

import pytest

from config_manager.postgres_loader import PostgresConfigLoader


@pytest.fixture
def loader():
    return PostgresConfigLoader(
        postgres_uri="postgresql://user:password@localhost:5432/testdb",
        app_name="TestApp",
        app_id="123e4567-e89b-12d3-a456-426614174000",
    )


@pytest.fixture
def loader_no_app_id():
    return PostgresConfigLoader(
        postgres_uri="postgresql://user:password@localhost:5432/testdb",
        app_name="TestAppTwo",
    )


@patch("config_manager.postgres_loader.psycopg2.connect")
def test_initialize_application(mock_connect, loader_no_app_id):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    loader_no_app_id.initialize_application()

    mock_connect.assert_called_with("postgresql://user:password@localhost:5432/testdb")
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("config_manager.postgres_loader.psycopg2.connect")
def test_load(mock_connect, loader):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("KEY1", "value1"), ("KEY2", "value2")]

    config = loader.load()

    mock_cursor.execute.assert_called_with(
        "\n                SELECT key, value FROM config\n                WHERE app_id = %s;\n            ",
        ("123e4567-e89b-12d3-a456-426614174000",),
    )
    assert config == {"KEY1": "value1", "KEY2": "value2"}
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("config_manager.postgres_loader.psycopg2.connect")
def test_save(mock_connect, loader):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    config = {"KEY1": "value1", "KEY2": "value2"}
    loader.save(config)

    # initialize_application is called within save
    assert (
        mock_cursor.execute.call_count == 2
    )  # 1 for initialize_application, 1 for config entry
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("config_manager.postgres_loader.psycopg2.connect")
def test_initialize_database(mock_connect, loader):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    loader.initialize_database()

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("config_manager.postgres_loader.psycopg2.connect")
def test_load_exception(mock_connect, loader):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Load error")

    with pytest.raises(Exception, match="Load error"):
        loader.load()


@patch("config_manager.postgres_loader.psycopg2.connect")
def test_save_exception(mock_connect, loader):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Save error")

    with pytest.raises(Exception, match="Save error"):
        loader.save({"KEY": "value"})


if __name__ == "__main__":
    pytest.main()
