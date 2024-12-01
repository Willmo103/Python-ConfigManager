import os

import pytest

from config_manager.env_loader import EnvConfigLoader


@pytest.fixture
def loader():
    return EnvConfigLoader()


def test_load_env(loader, monkeypatch):
    monkeypatch.setenv("TEST_KEY", "test_value")
    config = loader.load()
    assert config.get("TEST_KEY") == "test_value"


def test_save_env(loader, monkeypatch):
    loader.save({"NEW_KEY": "new_value"})
    assert os.getenv("NEW_KEY") == "new_value"


def test_load_with_dotenv(loader, tmp_path, monkeypatch):
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("DOTENV_KEY=dotenv_value")
    config = loader.load(file_path=str(dotenv_path))
    assert config.get("DOTENV_KEY") == "dotenv_value"


def test_save_env_overwrites(loader, monkeypatch):
    monkeypatch.setenv("OVERWRITE_KEY", "old_value")
    loader.save({"OVERWRITE_KEY": "new_value"})
    assert os.getenv("OVERWRITE_KEY") == "new_value"


def test_save_env_with_file(loader, tmp_path):
    env_path = tmp_path / ".env"
    loader.save(
        {"FILE_KEY": "file_value", "FILE_KEY2": 123, "FILE_KEY3": 3.14, "FILE_KEY4": True},
        file_path=str(env_path),
    )
    assert env_path.read_text() == "FILE_KEY=file_value\nFILE_KEY2=123\nFILE_KEY3=3.14\nFILE_KEY4=True\n"
    assert os.getenv("FILE_KEY") == "file_value"
    assert os.getenv("FILE_KEY2") == "123"
    assert os.getenv("FILE_KEY3") == "3.14"
    assert os.getenv("FILE_KEY4") == "True"

def test_saving_list_to_env_throws_not_implemented_error(loader):
    with pytest.raises(NotImplementedError):
        loader.save({"LIST_KEY": [1, 2, 3]}, file_path='test.env')

def test_saving_dict_to_env_throws_not_implemented_error(loader):
    with pytest.raises(NotImplementedError):
        loader.save({"DICT_KEY": {"key": "value"}}, file_path='test.env')

if __name__ == "__main__":
    pytest.main()
