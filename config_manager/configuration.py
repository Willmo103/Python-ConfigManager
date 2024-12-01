from typing import Any, Dict, Mapping, Optional

from .base_loader import BaseConfigLoader
from .env_loader import EnvConfigLoader
from .json_loader import JSONConfigLoader
from .postgres_loader import PostgresConfigLoader
from .sqlite_loader import SQLiteConfigLoader
from .yaml_loader import YAMLConfigLoader


class Configuration:
    def __init__(self, loader: BaseConfigLoader):
        self.loader = loader
        self.config = self.loader.load()

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
    def from_env(cls) -> "Configuration":
        loader = EnvConfigLoader()
        return cls(loader)

    @classmethod
    def from_json(
        cls, file_path: Optional[str] = None, json_data: Optional[str] = None
    ) -> "Configuration":
        loader = JSONConfigLoader(file_path=file_path, json_data=json_data)
        return cls(loader)

    @classmethod
    def from_yaml(
        cls, file_path: Optional[str] = None, yaml_data: Optional[str] = None
    ) -> "Configuration":
        loader = YAMLConfigLoader(file_path=file_path, yaml_data=yaml_data)
        return cls(loader)

    @classmethod
    def from_postgres(
        cls, postgres_uri: str, postgres_table: str = "config"
    ) -> "Configuration":
        loader = PostgresConfigLoader(
            postgres_uri=postgres_uri, postgres_table=postgres_table
        )
        return cls(loader)

    @classmethod
    def from_sqlite(cls, sqlite_location: str) -> "Configuration":
        loader = SQLiteConfigLoader(sqlite_location=sqlite_location)
        return cls(loader)

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
            postgres_uri=postgres_uri, postgres_table=postgres_table
        )
        loader.save(self.config)

    def to_sqlite(self, sqlite_location: str) -> None:
        loader = SQLiteConfigLoader(sqlite_location=sqlite_location)
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
        return Configuration(loader=self.loader.__class__(**self.loader.__dict__))
