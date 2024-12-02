# Release Notes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-04-27

### Added

- **Core Features**:
  - Initial release of Config Manager.
  - Support for multiple configuration formats:
    - JSON
    - YAML
    - Environment Variables
    - SQLite
    - PostgreSQL
  - Unique application identification using UUIDs.
  - Comprehensive `Configuration` class for managing configurations.
  - Modular loader classes inheriting from `BaseConfigLoader`.

- **Testing & Documentation**:
  - Comprehensive test suite achieving 100% coverage.
  - Detailed documentation and usage examples.

### Changed

- **Codebase**:
  - Refactored code for better modularity and maintainability.
  - Improved error handling across all modules.

### Fixed

- N/A

## [0.2.0] - 2024-05-15

### Added

- **New Features**:
  - Added support for custom configuration validation.
  - Introduced logging for configuration operations.
  
- **Enhancements**:
  - Improved performance for loading configurations from PostgreSQL.
  - Enhanced error messages for better debugging.

### Changed

- **Codebase**:
  - Refactored the `Configuration` class for better readability.
  - Updated dependencies to the latest stable versions.

### Fixed

- **Bug Fixes**:
  - Resolved an issue where saving to environment variables failed for non-string types.
  - Fixed a bug in `PostgresConfigLoader` that prevented proper initialization.

## [Unreleased]

### Added

- Future features and enhancements.

### Changed

- N/A

### Fixed

- N/A

---

**[0.1.0]: https://git.willmo.dev/USERNAME/Python-ConfigManager/releases/tag/v0.1.0**
**[0.2.0]: https://git.willmo.dev/USERNAME/Python-ConfigManager/releases/tag/v0.2.0**
