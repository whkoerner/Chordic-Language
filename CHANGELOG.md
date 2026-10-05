# Changelog

All meaningful Chordic language and research changes are recorded chronologically. Older entries should not be rewritten to make development appear cleaner than it was.

## [Unreleased]

### Added

- EXP-002 compact conversational candidate with 61 reusable symbolic tokens and compact grammar.
- 37-case common/normal/seed benchmark plus frozen Rocky CT2 timing provenance.
- Reproducible timing, round-trip, exact/near-collision, prefix, and critical-pair analysis.
- Automated EXP-002 tests and experiment report documenting accepted and rejected tradeoffs.
- Machine-readable v0.0 scaffolding for dictionary, grammar, phonology, gestures, and acceptance examples.
- All 11 required seed expressions as unsupported future acceptance targets with no invented translations.
- Data-model documentation defining how unresolved and unsupported information is represented.
- ADR-001 documenting the unresolved pitch-reference strategy and the evidence required before selection.
- EXP-001, the planned first comparison of pitch-reference approaches.
- 11 automated v0.0 data-integrity tests.
- GitHub Actions validation on pushes and pull requests.

### Changed

- Project status now distinguishes the preserved v0.0 baseline from the active v0.1-experimental candidate.
- Routine normal benchmark timing improved from 8.030 s mean / 10.875 s max to 6.794 s mean / 8.400 s max at unchanged Rocky 3× timing.
- README status now reports the actual v0.0 data/test state.
- Roadmap now moves completed foundation work out of Current and makes EXP-001 the active research step.

### Test results

- GitHub Actions run #1 passed on commit `ce26b17a402c942a4181c5ba2622bde8046d0d2e`.
- 11 data-integrity tests passed.
- Audio recognition, human production, translation, and usability remain untested.

### Experimental findings

- EXP-002 achieved 100% (17/17) of required normal benchmark cases at or below 10 seconds without reducing playback speed.
- Exact symbolic lexical collisions: 0; benchmark token-sequence collisions: 0.
- Short two-note forms still have distance-1 neighbors, so acoustic recognizability remains unproven.
- The long multi-clause historical seed remains over 20 seconds and was intentionally not replaced by an opaque sentence shortcut.
- EXP-001/acoustic follow-up remains required.

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
