"""
Package: config_manager
Module: configuration
This module contains the Configuration class that is used to manage application configurations.
"""

from typing import Any, Dict, Optional, Mapping
from .base_loader import BaseConfigLoader
from .env_loader import EnvConfigLoader
from .json_loader import JSONConfigLoader
from .yaml_loader import YAMLConfigLoader
from .postgres_loader import PostgresConfigLoader
from .sqlite_loader import SQLiteConfigLoader
import uuid


class Configuration:
    def __init__(self, loader: BaseConfigLoader, app_id: Optional[str] = None):
        self.loader = loader
        self.app_id = app_id or self._generate_uuid()
        self.config = self.loader.load()
        self.config["APP_ID"] = self.app_id  # Ensure APP_ID is always present

    def __repr__(self) -> str:
        items = [
            f"{key.upper().replace('_', '')}={value}"
            for key, value in self.config.items()
        ]
        out_s = "\n```toml\n"
        out_e = "\n```"
        return out_s + "\n".join(items) + out_e

    def __str__(self) -> str:
        return self.__repr__()

    def __getitem__(self, key: str) -> Any:
        return self.config.get(key, "")

    def __setitem__(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.loader.save(self.config)

    def __delitem__(self, key: str) -> None:
        if key in self.config:
            del self.config[key]
            self.loader.save(self.config)

    def __contains__(self, key: str) -> bool:
        return key in self.config

    def __iter__(self):
        return iter(self.config.items())

    def __len__(self) -> int:
        return len(self.config)

    def __bool__(self) -> bool:
        return bool(self.config)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Configuration):
            return False
        return self.config == other.config

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.config.items())))

    @classmethod
    def initialize(cls, config_type: str, app_name: str, **kwargs) -> "Configuration":
        """
        Initialize a new application with the given app_name and configuration type.

        Args:
            config_type (str): Type of configuration ('env', 'json', 'yaml', 'postgres', 'sqlite').
            app_name (str): Name of the application.
            **kwargs: Additional arguments required by the loader.

        Returns:
            Configuration: An instance of Configuration.
        """
        app_id = str(uuid.uuid4())
        loader = cls._get_loader(
            config_type, app_name=app_name, app_id=app_id, **kwargs
        )
        config = cls(loader, app_id=app_id)
        config["APP_NAME"] = app_name  # Store app_name in config
        return config

    @classmethod
    def _get_loader(
        cls, config_type: str, app_name: str, app_id: str, **kwargs
    ) -> BaseConfigLoader:
        if config_type == "env":
            return EnvConfigLoader()
        elif config_type == "json":
            return JSONConfigLoader(
                file_path=kwargs.get("file_path"), json_data=kwargs.get("json_data")
            )
        elif config_type == "yaml":
            return YAMLConfigLoader(
                file_path=kwargs.get("file_path"), yaml_data=kwargs.get("yaml_data")
            )
        elif config_type == "postgres":
            postgres_uri = kwargs.get("postgres_uri")
            postgres_table = kwargs.get("postgres_table", "config")
            return PostgresConfigLoader(
                postgres_uri=postgres_uri,
                app_name=app_name,
                app_id=app_id,
                postgres_table=postgres_table,
            )
        elif config_type == "sqlite":
            sqlite_location = kwargs.get("sqlite_location")
            return SQLiteConfigLoader(
                sqlite_location=sqlite_location, app_name=app_name, app_id=app_id
            )
        else:
            raise ValueError(f"Unsupported configuration type: {config_type}")

    @classmethod
    def load_existing(cls, config_type: str, app_id: str, **kwargs) -> "Configuration":
        """
        Load an existing application's configuration using app_id.

        Args:
            config_type (str): Type of configuration ('env', 'json', 'yaml', 'postgres', 'sqlite').
            app_id (str): UUID of the application.
            **kwargs: Additional arguments required by the loader.

        Returns:
            Configuration: An instance of Configuration.
        """
        loader = cls._get_loader(config_type, app_name="", app_id=app_id, **kwargs)
        return cls(loader, app_id=app_id)

    @staticmethod
    def _generate_uuid() -> str:
        return str(uuid.uuid4())

    def to_json(self, file_path: Optional[str] = None) -> Optional[str]:
        loader = JSONConfigLoader(file_path=file_path)
        loader.save(self.config)
        if not file_path:
            import json

            return json.dumps(self.config, indent=4)
        return None

    def to_yaml(self, file_path: Optional[str] = None) -> Optional[str]:
        loader = YAMLConfigLoader(file_path=file_path)
        loader.save(self.config)
        if not file_path:
            import yaml

            return yaml.dump(self.config, default_flow_style=False)
        return None

    def to_env(self) -> None:
        loader = EnvConfigLoader()
        loader.save(self.config)

    def to_postgres(self, postgres_uri: str, postgres_table: str = "config") -> None:
        loader = PostgresConfigLoader(
            postgres_uri=postgres_uri,
            app_name=self.config.get("APP_NAME", "default"),
            app_id=self.app_id,
            postgres_table=postgres_table,
        )
        loader.save(self.config)

    def to_sqlite(self, sqlite_location: str) -> None:
        loader = SQLiteConfigLoader(
            sqlite_location=sqlite_location,
            app_name=self.config.get("APP_NAME", "default"),
            app_id=self.app_id,
        )
        loader.save(self.config)

    def to_dict(self) -> Dict[str, Any]:
        return self.config.copy()

    def update(self, config: Mapping[str, Any]) -> None:
        self.config.update(config)
        self.loader.save(self.config)

    def clear(self) -> None:
        self.config.clear()
        self.loader.save(self.config)

    def copy(self) -> "Configuration":
        return Configuration(
            loader=self.loader.__class__(**self.loader.__dict__), app_id=self.app_id
        )
