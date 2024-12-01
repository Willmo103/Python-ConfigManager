# tests/test_configuration.py

from unittest.mock import MagicMock, patch

import pytest

from config_manager.base_loader import BaseConfigLoader
from config_manager.configuration import Configuration


@pytest.fixture
def mock_loader():
    loader = MagicMock(spec=BaseConfigLoader)
    loader.load.return_value = {"KEY1": "value1", "KEY2": "value2"}
    return loader


def test_configuration_initialization(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    assert config.app_id == "test-app-id"
    assert config.config == {
        "KEY1": "value1",
        "KEY2": "value2",
        "APP_ID": "test-app-id",
    }
    mock_loader.load.assert_called_once()


def test_configuration_repr(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    expected_repr = "\n```toml\nKEY1=value1\nKEY2=value2\nAPP_ID=test-app-id\n```"
    assert repr(config) == expected_repr


def test_configuration_str(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    expected_str = "\n```toml\nKEY1=value1\nKEY2=value2\nAPP_ID=test-app-id\n```"
    assert str(config) == expected_str


def test_get_item(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    assert config["KEY1"] == "value1"
    assert config["NON_EXISTENT"] == ""


def test_set_item(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    config["KEY3"] = "value3"
    assert config.config["KEY3"] == "value3"
    mock_loader.save.assert_called_with(config.config)


def test_del_item(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    del config["KEY1"]
    assert "KEY1" not in config.config
    mock_loader.save.assert_called_with(config.config)


def test_contains(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    assert "KEY1" in config
    assert "NON_EXISTENT" not in config


def test_iter(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    items = list(iter(config))
    expected_items = [("KEY1", "value1"), ("KEY2", "value2"), ("APP_ID", "test-app-id")]
    assert items == expected_items


def test_len(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    assert len(config) == 3


def test_bool(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    assert bool(config) is True
    config.clear()
    assert bool(config) is False


def test_eq(mock_loader):
    config1 = Configuration(loader=mock_loader, app_id="test-app-id")
    config2 = Configuration(
        loader=MagicMock(spec=BaseConfigLoader), app_id="test-app-id"
    )
    config2.config = {"KEY1": "value1", "KEY2": "value2", "APP_ID": "test-app-id"}
    assert config1 == config2


def test_hash(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    assert isinstance(hash(config), int)


@patch("config_manager.configuration.Configuration._get_loader")
@patch("config_manager.configuration.uuid.uuid4")
def test_initialize(mock_uuid, mock_get_loader, mock_loader):
    mock_uuid.return_value = "generated-uuid"
    mock_get_loader.return_value = MagicMock(spec=BaseConfigLoader)
    config = Configuration.initialize(
        config_type="json", app_name="TestApp", file_path="config.json"
    )
    assert config.app_id == "generated-uuid"
    # assert config.config.get("APP_NAME") == "TestApp"
    mock_get_loader.assert_called_once()


@patch("config_manager.configuration.Configuration._get_loader")
def test_load_existing(mock_get_loader, mock_loader):
    mock_get_loader.return_value = MagicMock(spec=BaseConfigLoader)
    config = Configuration.load_existing(
        config_type="yaml", app_id="existing-app-id", file_path="config.yaml"
    )
    assert config.app_id == "existing-app-id"
    mock_get_loader.assert_called_once()


def test_to_dict(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    config_dict = config.to_dict()
    expected = {"KEY1": "value1", "KEY2": "value2", "APP_ID": "test-app-id"}
    assert config_dict == expected


def test_update(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    config.update({"KEY3": "value3"})
    assert config.config["KEY3"] == "value3"
    mock_loader.save.assert_called_with(config.config)


def test_clear(mock_loader):
    config = Configuration(loader=mock_loader, app_id="test-app-id")
    config.clear()
    assert config.config == {}
    mock_loader.save.assert_called_with(config.config)


# def test_copy(mock_loader):
#     config = Configuration(loader=mock_loader, app_id="test-app-id")
#     copied_config = config.copy()
#     assert copied_config.config == config.config
#     assert copied_config.app_id == config.app_id
#     assert copied_config.loader == config.loader

if __name__ == "__main__":
    pytest.main()
