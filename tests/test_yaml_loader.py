import yaml
import pytest
from config_manager.yaml_loader import YAMLConfigLoader

@pytest.fixture
def sample_yaml():
    return {"key1": "value1", "key2": "value2"}

def test_load_yaml_file(sample_yaml, tmp_path):
    yaml_path = tmp_path / "config.yaml"
    yaml_path.write_text(yaml.dump(sample_yaml))
    loader = YAMLConfigLoader(file_path=str(yaml_path))
    config = loader.load()
    assert config == sample_yaml

def test_load_yaml_data(sample_yaml):
    yaml_data = yaml.dump(sample_yaml)
    loader = YAMLConfigLoader(yaml_data=yaml_data)
    config = loader.load()
    assert config == sample_yaml

def test_save_yaml_file(sample_yaml, tmp_path):
    yaml_path = tmp_path / "output.yaml"
    loader = YAMLConfigLoader(file_path=str(yaml_path))
    loader.save(sample_yaml)
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    assert data == sample_yaml

def test_save_yaml_without_file():
    loader = YAMLConfigLoader()
    with pytest.raises(ValueError):
        loader.save({"key": "value"})

if __name__ == '__main__':
    pytest.main()