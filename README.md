# Chordic Language

Chordic is an experimental tonal constructed-language research project. The goal is to develop, from first principles, a communication system that can eventually be human-producible, human-learnable, computer-recognizable, compositional, deterministic enough to parse, and useful for robotic communication.

The repository is intentionally starting at **v0.0 — Concept**. It is not a finished language. Git history, failed experiments, revisions, decision records, tests, and negative results are part of the research record.

Chordic is inspired by the idea of tonal communication associated with Rocky in *Project Hail Mary*, but this project is developing its own original, testable system. Short user-provided expressions are retained only as communication goals and acceptance examples, not as an attempt to reproduce another work's language.

## Current status

| Metric | Status |
| --- | --- |
| Current language version | v0.0 — Concept |
| Primitive concepts | 0 |
| Grammar rules | 0 |
| Canonical tonal forms | 0 |
| Automated tests | 11 data-integrity tests |
| Known tonal collisions | Not yet tested. |
| Reserved forms | 0 |
| Human recognition accuracy | Not yet tested. |
| Machine-generated recognition accuracy | Not yet tested. |
| Human-generated recognition accuracy | Not yet tested. |

The 11 current tests validate the v0.0 machine-readable data and repository invariants. They do **not** establish that Chordic audio, recognition, translation, or human usability works.

### Known limitations

- Phonology: Not yet determined.
- Pitch reference strategy: Not yet determined.
- Word boundaries: Not yet determined.
- Grammar: Not yet determined.
- Dictionary: no canonical primitives have been defined.
- Synthesis: Not yet implemented.
- Recognition: Not yet implemented.
- Translation: Not yet implemented.
- Human usability: Not yet tested.

## Development principle

Chordic should develop through evidence:

**concept → design → experiments → failures → revisions → testing → working language**

Important language behavior should not be silently replaced. When a major rule changes, preserve the old state in Git history, document the problem, record the decision, add or update tests when practical, and update the changelog.

See [docs/development-principles.md](docs/development-principles.md) for the working process, [ROADMAP.md](ROADMAP.md) for project state, and [CHANGELOG.md](CHANGELOG.md) for chronological changes.

## Repository map

- `docs/history/` — version notes and historical context
- `docs/decisions/` — Language/Architecture Decision Records
- `docs/specifications/` — current specifications and data-model documentation
- `docs/experiments/` — experiment plans and interpreted results
- `language/` — machine-readable canonical language data
- `tests/` — automated validation and later linguistic/recognition tests
- `tools/` — translator, synthesizer, recognizer, and research utilities when justified
- `experiments/` — raw experiment artifacts and data when they exist

Directories are added when needed rather than populated with fake complexity.

## Versioning

Language versions represent capability/specification milestones, not repository activity. Adding files or code does not automatically advance the language.

The current experimental language version remains **v0.0 — Concept** until evidence justifies a milestone change.

## Running tests

From the repository root, run:

```bash
python -m unittest discover -s tests -v
```

The same suite runs automatically through GitHub Actions on pushes and pull requests.

## Licensing

This repository uses split licensing:

- Software, tools, tests, and source code: MIT License.
- Language specification, dictionary/language data, documentation, examples, and research/experiment content: Creative Commons Attribution 4.0 International (CC BY 4.0).

See [LICENSE.md](LICENSE.md) for scope details.
