import json
import pytest
from config_manager.json_loader import JSONConfigLoader

@pytest.fixture
def sample_json():
    return {"KEY1": "value1", "KEY2": "value2"}

def test_load_json_file(sample_json, tmp_path):
    json_path = tmp_path / "config.json"
    json_path.write_text(json.dumps(sample_json))
    loader = JSONConfigLoader(file_path=str(json_path))
    config = loader.load()
    assert config == sample_json

def test_load_json_data(sample_json):
    json_data = json.dumps(sample_json)
    loader = JSONConfigLoader(json_data=json_data)
    config = loader.load()
    assert config == sample_json

def test_save_json_file(sample_json, tmp_path):
    json_path = tmp_path / "output.json"
    loader = JSONConfigLoader(file_path=str(json_path))
    loader.save(sample_json)
    with open(json_path, "r") as f:
        data = json.load(f)
    assert data == sample_json

def test_save_json_without_file():
    loader = JSONConfigLoader()
    with pytest.raises(ValueError):
        loader.save({"key": "value"})

if __name__ == '__main__':
    pytest.main()