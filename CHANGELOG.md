# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-09-29
### Added
- Support passing full YouTube URLs (`watch?v=`, `youtu.be/`) via new normalization helper.

### Fixed
- Editable install/build failure with newer setuptools by removing deprecated license classifier.
- Output directory now expands `~` reliably.

### Notes
- Tagging as 0.2.1 to avoid retagging 0.2.0.

## [0.2.0] - 2025-09-29
### Added
- Adaptive transcript fetching and formatter compatibility improvements.
- Pre-commit configuration with ruff lint/format and hygiene hooks.
- Development workflow documentation in README.
- Continuous Integration workflow (lint, format check, tests) via GitHub Actions.

### Changed
- Standardized tooling on `uv`; removed prior Rye configuration.
- Minor code formatting and typing refinements.

### Notes
- No breaking changes. CLI usage unchanged.

## [0.1.0] - 2025-09-??
### Added
- Initial release with CLI to fetch manually created English YouTube transcripts and output Markdown.
