"""
Package: config_manager
Module: env_loader
This module contains the EnvConfigLoader class that is used to load and save configuration data from environment variables.
"""

import os
from typing import Any, Dict

from dotenv import load_dotenv

from .base_loader import BaseConfigLoader


class EnvConfigLoader(BaseConfigLoader):
    """
    Configuration loader for environment variables.
    """

    def load(self, file_path: str | None = None) -> Dict[str, Any]:
        """
        Load configuration data from environment variables.
        :param file_path: Path to .env file. default is `None`.
        :return: Dict containing configuration data.
        """
        if file_path:
            load_dotenv(file_path)
        else:
            load_dotenv()
        return dict(os.environ)

    def save(
        self, config: Dict[str, Any], file_path: str | None = None
    ) -> None | NotImplementedError:
        """
        Save configuration data to environment variables.
        :param config: A dict containing configuration data.
        :param file_path: Path to .env file. default is `None`.
        :return: None
        """
        if file_path:
            with open(file_path, "w") as f:
                for key, value in config.items():
                    if (
                        isinstance(value, str)
                        or isinstance(value, int)
                        or isinstance(value, float)
                        or isinstance(value, bool)
                    ):
                        f.write(f"{key.upper().replace(' ', '_').strip()}={value}\n")
                    else:
                        raise NotImplementedError(
                            f"Data type {type(value)} not yet supported for saving to .env file."
                        )
        for key, value in config.items():
            os.environ[key] = str(value)
        return
