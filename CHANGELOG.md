# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Target `youtube-transcript-api` 1.x exclusively (dependency floor raised to `>=1.0`; the old `>=0.6.2` floor was broken — `CouldNotRetrieveTranscript` does not exist in 0.6.x).
- `get` now validates the video id / URL up front and exits with a friendly message instead of an opaque API error.
- URL normalization also handles `shorts/`, `embed/`, `watch/`, `v/`, and `live/` path forms; unrecognized URLs are rejected.
- `-o/--output` now defaults to the working directory at invocation time instead of import time.
- Output log message shows the full file path instead of the directory.

### Fixed
- Formatter crash on string timestamps (`int(float(start))` conversion).
- Error exits use `ctx.exit(1)` instead of raising `click.exceptions.Exit` directly.

### Removed
- Dead `YouTubeTranscriptApi.list_transcripts` class-method branch (removed upstream in v1.0) and the `find_transcript` fallback that could silently return auto-generated transcripts.

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
