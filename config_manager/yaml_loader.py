"""
Package: config_manager
Module: yaml_loader
This module contains the YAMLConfigLoader class that is used to load and save configuration data from YAML files.
"""

from typing import Any, Dict, Optional

import yaml

from .base_loader import BaseConfigLoader


class YAMLConfigLoader(BaseConfigLoader):
    """
    Configuration loader for YAML files.
    """

    def __init__(
        self, file_path: Optional[str] = None, yaml_data: Optional[str] = None
    ):
        """
        Initialize YAMLConfigLoader with file path and YAML data.
        :param file_path: Path to YAML file.
        :param yaml_data: YAML data.
        """
        self.file_path = file_path
        self.yaml_data = yaml_data

    def load(self) -> Dict[str, Any]:
        """
        Load configuration data from YAML file.
        :return: Dict containing configuration data.
        """
        if self.yaml_data:
            return yaml.safe_load(self.yaml_data) or {}
        if not self.file_path:
            raise ValueError("File path must be provided for YAMLConfigLoader.")
        with open(self.file_path, "r") as file:
            return yaml.safe_load(file) or {}

    def save(self, config: Dict[str, Any]) -> None:
        """
        Save configuration data to YAML file.
        :param config: A dict containing configuration data.
        :return: None
        """
        if not self.file_path:
            raise ValueError("File path must be provided for YAMLConfigLoader.")
        with open(self.file_path, "w") as file:
            yaml.dump(config, file, default_flow_style=False)
