# Config Manager

[![PyPI Version](https://img.shields.io/pypi/v/config_manager.svg)](https://pypi.org/project/config_manager/)
[![License](https://img.shields.io/pypi/l/config_manager.svg)](https://github.com/willmo103/Python-ConfigManager/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/config_manager.svg)](https://python.org/downloads/)
[![Coverage Status](https://img.shields.io/coveralls/github/willmo103/Python-ConfigManager.svg)](https://coveralls.io/github/willmo103/Python-ConfigManager)

Config Manager is a modular configuration management system for Python applications. It supports multiple configuration formats including JSON, YAML, environment variables, SQLite, and PostgreSQL databases. Each application managed by Config Manager is uniquely identified by a UUID, ensuring isolated and secure configuration management.

## Features

- **Multiple Configuration Formats**: JSON, YAML, Environment Variables, SQLite, PostgreSQL.
- **Application-Specific Configurations**: Each application has a unique UUID and name.
- **Easy Initialization**: Simple methods to initialize and load configurations.
- **Extensible Design**: Easily add support for new configuration formats.
- **Comprehensive Error Handling**: Gracefully handle exceptions and errors.
- **100% Test Coverage**: Reliable and robust with comprehensive tests.

## Installation

You can install Config Manager via `pip`:

```bash
pip install config_manager
```

Or install it from the source:

```bash
git clone https://git.willmo.dev/willmo103/Python-ConfigManager.git
cd Python-ConfigManager
pip install .
```

For development purposes, install in editable mode:

```bash
pip install -e .
```

## Usage

### 1. Initializing a New Application Configuration

```python
from config_manager import Configuration

# Initialize a new application with a JSON backend
config = Configuration.initialize(
    config_type='json',
    app_name='MyApp',
    file_path='config.json'
)

# Access configuration values
db_host = config["DB_HOST"]
print(f"Database Host: {db_host}")

# Set a new configuration value
config["NEW_KEY"] = "new_value"

# Save configuration to JSON file
config.to_json(file_path='updated_config.json')
```

### 2. Loading an Existing Application's Configuration

```python
from config_manager import Configuration

# Load existing configuration using app_id
app_id = '123e4567-e89b-12d3-a456-426614174000'
config = Configuration.load_existing(
    config_type='json',
    app_id=app_id,
    file_path='config.json'
)

# Access and update configuration values
api_key = config.get("API_KEY", "")
config["API_KEY"] = "new_api_key_value"

# Save updates
config.to_json(file_path='config.json')
```

### 3. Using Different Configuration Backends

#### a. Environment Variables

```python
from config_manager import Configuration

config = Configuration.initialize(
    config_type='env',
    app_name='EnvApp'
)

config["ENV_KEY"] = "env_value"
config.to_env()

print(config["ENV_KEY"])  # Outputs: env_value
```

#### b. YAML Files

```python
from config_manager import Configuration

config = Configuration.initialize(
    config_type='yaml',
    app_name='YamlApp',
    file_path='config.yaml'
)

config["YAML_KEY"] = "yaml_value"
config.to_yaml(file_path='config.yaml')
```

#### c. PostgreSQL Database

```python
from config_manager import Configuration

config = Configuration.initialize(
    config_type='postgres',
    app_name='PostgresApp',
    postgres_uri='postgresql://user:password@localhost:5432/mydatabase',
    postgres_table='config'
)

config["DB_HOST"] = "localhost"
config.to_postgres(
    postgres_uri='postgresql://user:password@localhost:5432/mydatabase',
    postgres_table='config'
)
```

#### d. SQLite Database

```python
from config_manager import Configuration

config = Configuration.initialize(
    config_type='sqlite',
    app_name='SQLiteApp',
    sqlite_location='config.db'
)

config["SQLITE_KEY"] = "sqlite_value"
config.to_sqlite(sqlite_location='config.db')
```

### 4. Accessing and Modifying Configurations

```python
# Accessing configuration values
value = config["KEY_NAME"]

# Setting configuration values
config["KEY_NAME"] = "new_value"

# Deleting configuration keys
del config["KEY_NAME"]

# Iterating over configurations
for key, value in config:
    print(f"{key}: {value}")

# Converting to dictionary
config_dict = config.to_dict()

# Updating multiple configurations
config.update({"KEY1": "value1", "KEY2": "value2"})

# Clearing all configurations
config.clear()

# Creating a copy of the configuration
config_copy = config.copy()
```

## API Reference

### `Configuration` Class

#### Methods

- `initialize(config_type: str, app_name: str, **kwargs) -> Configuration`
  - Initialize a new application configuration.
  
- `load_existing(config_type: str, app_id: str, **kwargs) -> Configuration`
  - Load an existing application's configuration using `app_id`.
  
- `__getitem__(key: str) -> Any`
  - Get the value associated with `key`.
  
- `__setitem__(key: str, value: Any) -> None`
  - Set the value for `key`.
  
- `__delitem__(key: str) -> None`
  - Delete the configuration entry for `key`.
  
- `__contains__(key: str) -> bool`
  - Check if `key` exists in the configuration.
  
- `__iter__()`
  - Iterate over configuration items.
  
- `__len__() -> int`
  - Get the number of configuration items.
  
- `__bool__() -> bool`
  - Check if the configuration is not empty.
  
- `to_json(file_path: Optional[str] = None) -> Optional[str]`
  - Save configuration to a JSON file or return as a JSON string.
  
- `to_yaml(file_path: Optional[str] = None) -> Optional[str]`
  - Save configuration to a YAML file or return as a YAML string.
  
- `to_env() -> None`
  - Save configuration to environment variables.
  
- `to_postgres(postgres_uri: str, postgres_table: str = "config") -> None`
  - Save configuration to a PostgreSQL database.
  
- `to_sqlite(sqlite_location: str) -> None`
  - Save configuration to a SQLite database.
  
- `to_dict() -> Dict[str, Any]`
  - Convert configuration to a dictionary.
  
- `update(config: Mapping[str, Any]) -> None`
  - Update configuration with multiple key-value pairs.
  
- `clear() -> None`
  - Clear all configuration entries.
  
- `copy() -> Configuration`
  - Create a copy of the current configuration.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

Please ensure that all tests pass and that the code adheres to the project's coding standards.

## License

This project is licensed under the [MIT License](https://github.com/willmo103/Python-ConfigManager/blob/main/LICENSE).

## Contact

For any inquiries or support, please contact:

**Will Morris**  
Email: [willmorris188@gmail.com](mailto:willmorris188@gmail.com)  
GitHub: [willmo103](https://git.willmo.dev/willmo103/Python-ConfigManager)

## Acknowledgements

- [psycopg2](https://pypi.org/project/psycopg2-binary/)
- [PyYAML](https://pypi.org/project/PyYAML/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [pytest](https://docs.pytest.org/en/stable/)
```

---

## 3. Release Notes

Create a `RELEASE_NOTES.md` file to document changes between versions. Here's a template you can use:

```markdown
# Release Notes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-04-27

### Added

- Initial release of Config Manager.
- Support for loading and saving configurations in JSON, YAML, Environment Variables, SQLite, and PostgreSQL.
- Unique application identification using UUIDs.
- Comprehensive `Configuration` class for managing configurations.
- Modular loader classes inheriting from `BaseConfigLoader`.
- Comprehensive test suite achieving 100% coverage.
- Documentation and usage examples.

### Changed

- Refactored codebase for better modularity and maintainability.
- Improved error handling across all modules.

### Fixed

- N/A

## [Unreleased]

### Added

- Future features and enhancements.

### Changed

- N/A

### Fixed

- N/A

---

**[0.1.0]: https://github.com/willmo103/Python-ConfigManager/releases/tag/0.1.0**
```
