# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet.

### Changed
- GitHub owner URLs now use `TheCleverJay/agent-ops-cli`.

## [0.1.0] — 2026-10-27

### Added
- Initial public release: `budget`, `watch`, `env-audit`, `log-digest`, `health`, `routine-lint`.
- Hard timeout / stall exit codes (124 / 125); missing binary returns 127 without traceback.
- Stdlib-only; bilingual README + docs; smoke tests.
