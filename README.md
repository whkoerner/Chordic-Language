# Chordic Language

Chordic is an experimental tonal constructed-language research project. The goal is to develop, from first principles, a communication system that can eventually be human-producible, human-learnable, computer-recognizable, compositional, deterministic enough to parse, and useful for robotic communication.

The repository intentionally preserves **v0.0 — Concept** as its starting baseline. It is not a finished language; EXP-002 now adds an active **v0.1-experimental** symbolic candidate without erasing that origin. Git history, failed experiments, revisions, decision records, tests, and negative results are part of the research record.

Chordic is inspired by the idea of tonal communication associated with Rocky in *Project Hail Mary*, but this project is developing its own original, testable system. Short user-provided expressions are retained only as communication goals and acceptance examples, not as an attempt to reproduce another work's language.

## Current status

| Metric | Status |
| --- | --- |
| Stable baseline | v0.0 — Concept |
| Active experimental candidate | v0.1-experimental / EXP-002 |
| Candidate reusable tokens | 61 |
| Candidate routine benchmark | 17/17 normal cases ≤10 s at Rocky 3× |
| Candidate normal mean | 6.794 s (CT2 baseline 8.030 s) |
| Exact candidate lexical collisions | 0 in symbolic analysis |
| Acoustic recognition | Not yet tested |
| Reserved forms | 0 |
| Human recognition accuracy | Not yet tested. |
| Machine-generated recognition accuracy | Not yet tested. |
| Human-generated recognition accuracy | Not yet tested. |

The original v0.0 integrity tests remain. EXP-002 adds benchmark/timing/collision tests for a separate candidate profile. Passing them establishes symbolic structure and timing evidence only; it does **not** establish microphone recognition, human production/listening accuracy, or general free-English translation.

### Known limitations

- Stable/canonical phonology: not yet established; EXP-002 defines only a symbolic candidate profile.
- Pitch reference strategy: still unresolved; the current note mapping exists for Rocky-compatible synthesis/timing experiments.
- Boundaries: EXP-002 retains explicit token boundaries, but human/acoustic boundary recognition is not validated.
- Grammar: EXP-002 has a compact candidate grammar; no grammar is stable yet.
- Dictionary: EXP-002 has 61 candidate tokens; no vocabulary is stable/canonical yet.
- Synthesis: Rocky-compatible timing/pitch mapping is defined for experiments, not as a final Chordic synthesizer.
- Recognition: microphone and human-produced recognition are not implemented or validated.
- Translation: benchmark intents have registered round trips; general free-English translation is not implemented.
- Human usability: not yet tested.

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

**v0.0 — Concept** remains the preserved baseline. **v0.1-experimental / EXP-002** is the active candidate profile because it has measured symbolic timing evidence, but it is not stable and is not acoustically validated. See `language/candidates/exp-002-compact-conversation.json` and `docs/experiments/EXP-002-conversation-speed.md`.

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
