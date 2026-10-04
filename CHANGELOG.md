# Changelog

All meaningful Chordic language and research changes are recorded chronologically. Older entries should not be rewritten to make development appear cleaner than it was.

## [Unreleased]

### Added

- Machine-readable v0.0 scaffolding for dictionary, grammar, phonology, gestures, and acceptance examples.
- All 11 required seed expressions as unsupported future acceptance targets with no invented translations.
- Data-model documentation defining how unresolved and unsupported information is represented.
- ADR-001 documenting the unresolved pitch-reference strategy and the evidence required before selection.
- EXP-001, the planned first comparison of pitch-reference approaches.
- 11 automated v0.0 data-integrity tests.
- GitHub Actions validation on pushes and pull requests.

### Changed

- README status now reports the actual v0.0 data/test state.
- Roadmap now moves completed foundation work out of Current and makes EXP-001 the active research step.

### Test results

- GitHub Actions run #1 passed on commit `ce26b17a402c942a4181c5ba2622bde8046d0d2e`.
- 11 data-integrity tests passed.
- Audio recognition, human production, translation, and usability remain untested.

### Experimental findings

- Not yet tested. EXP-001 is planned but has not been run.

### Known limitations

- Chordic still has no defined phonology, grammar, canonical vocabulary, synthesis, recognition, or translation system.
- Collision tests currently protect future machine-readable invariants but have no canonical tonal forms to evaluate yet.
- No human or acoustic evidence exists yet.

## [0.0] — 2026-10-04 — Concept

### Added

- Chordic Language project identity and purpose.
- Evidence-driven development philosophy.
- Explicit v0.0 — Concept starting point.
- Roadmap and history-preservation rules.
- Split licensing policy for software and language/research content.

### Changed

- Replaced the initial one-line repository README with an explicit research-project foundation.

### Deprecated

- Nothing.

### Removed

- Nothing.

### Fixed

- Nothing.

### Test results

- Not yet tested.

### Experimental findings

- Not yet tested.

### Known limitations

- No language behavior has been defined yet.
- No human or machine recognition experiments have been run.
