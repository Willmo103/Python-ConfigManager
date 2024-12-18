"""
Package: config_manager
Module: json_loader
This module contains the JSONConfigLoader class that is used to load and save configuration data from JSON files.
"""

import json
from typing import Any, Dict, Optional

from .base_loader import BaseConfigLoader


class JSONConfigLoader(BaseConfigLoader):
    """Configuration loader for JSON files."""

    def __init__(
        self, file_path: Optional[str] = None, json_data: Optional[str] = None
    ):
        """
        Initialize JSONConfigLoader with file path and JSON data.
        :param file_path: Path to JSON file.
        :param json_data: JSON data.
        """
        self.file_path = file_path
        self.json_data = json_data

    def load(self) -> Dict[str, Any]:
        """
        Load configuration data from JSON file.
        :return: Dict containing configuration data.
        """
        if self.json_data:
            return json.loads(self.json_data)
        if not self.file_path:
            raise ValueError("File path must be provided for JSONConfigLoader.")
        with open(self.file_path, "r") as file:
            return json.load(file)

    def save(self, config: Dict[str, Any]) -> str | None:
        """
        Save configuration data to JSON file.
        :param config: A dict containing configuration data.
        :return: None
        """
        if not self.file_path:
            # raise ValueError("File path must be provided for JSONConfigLoader.")
            return json.dumps(config)
        with open(self.file_path, "w") as file:
            json.dump(config, file, indent=4)  # noqa
