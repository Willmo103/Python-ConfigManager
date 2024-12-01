from abc import ABC

import pytest
from config_manager.base_loader import BaseConfigLoader


def test_base_loader_instantiation():
    with pytest.raises(TypeError):
        BaseConfigLoader()


def test_base_loader_methods():
    class TestLoader(BaseConfigLoader):
        def load(self):
            return {}

        def save(self, config):
            pass

    loader = TestLoader()
    assert loader.load() == {}
    loader.save({"key": "value"})  # Should not raise


def test_base_loader_abstract_methods():
    class TestLoader(BaseConfigLoader):
        pass

    with pytest.raises(TypeError):
        loader = TestLoader()
        loader.load()

    with pytest.raises(TypeError):
        loader = TestLoader()
        loader.save({})

if __name__ == "__main__":
    pytest.main()