"""
A simple configuration manager for Python applications.

This package provides a simple way to load and save configuration data from various sources such as JSON, YAML, environment variables, SQLite, and PostgreSQL databases.

The package is designed to be easy to use and flexible, allowing you to choose the configuration source that best fits your needs.

Example usage:

```python
from config_manager import Configuration, JSONConfigLoader


# Load configuration data from a JSON file
loader = JSONConfigLoader("config.json")
config = Configuration(loader)
data = config.load()

# Access configuration data
print(data.get("key"))

# Update configuration data["key"] = "new_value"
config.save(data)
```

For more information, please refer to the documentation at https://git.willmo.dev/willmo103/Python-ConfigManager

"""

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
