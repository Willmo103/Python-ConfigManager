"""
Package: config_manager
Module: base_loader
This module contains the BaseConfigLoader class that is used to load and save configuration data.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseConfigLoader(ABC):
    """
    Base class for configuration loaders
    """

    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """
        Load configuration data.
        :return: Dict containing configuration data.
        """
        pass

    @abstractmethod
    def save(self, config: Dict[str, Any]) -> None:
        """
        Save configuration data.
        :param config:
        :return: None
        """
        pass
