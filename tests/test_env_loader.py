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

if __name__ == "__main__":
    pytest.main()