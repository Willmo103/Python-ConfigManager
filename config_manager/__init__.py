from .configuration import Configuration
from .env_loader import EnvConfigLoader
from .json_loader import JSONConfigLoader
from .postgres_loader import PostgresConfigLoader
from .sqlite_loader import SQLiteConfigLoader
from .yaml_loader import YAMLConfigLoader

__all__ = [
    "Configuration",
    "EnvConfigLoader",
    "JSONConfigLoader",
    "YAMLConfigLoader",
    "PostgresConfigLoader",
    "SQLiteConfigLoader",
]

__package__ = "config_manager"
__version__ = "0.1.0"
__author__ = "Will Morris"
__author_email__ = "Willmorris188@gmail.com"
__description__ = "A simple configuration manager for Python applications."
__license__ = "MIT"
__url__ = "https://git.willmo.dev/willmo103/Python-ConfigManager"
