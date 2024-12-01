"""
Path: config_manager/base_loader.py
Description: Base class for configuration loaders.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseConfigLoader(ABC):
    """Base class for configuration loaders."""
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Load configuration data."""
        pass

    @abstractmethod
    def save(self, config: Dict[str, Any]) -> None:
        """Save configuration data."""
        pass
