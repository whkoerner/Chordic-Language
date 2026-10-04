# Development Principles

## Purpose

Chordic is being developed as an inspectable research and engineering project. The repository should show how the language changes, including wrong turns and negative results.

## Preserve history

For an important language-rule change:

1. Preserve the prior state through Git history.
2. Document the observed problem.
3. Record the proposed change.
4. Add or update tests that demonstrate the problem when practical.
5. Update the current specification.
6. Update the changelog.
7. Update roadmap/status information when project state changes.
8. Make a descriptive commit.

Do not rewrite old decision records to make past reasoning appear cleaner. If a decision is reversed, create a new record that supersedes and references the old one.

## Decision records

Major language or architecture choices belong in `docs/decisions/`.

A decision record should include:

- Context
- Problem
- Options considered
- Decision
- Reason
- Consequences
- Evidence or experiments

A decision may explicitly defer a choice when evidence is missing.

## Experiments

Meaningful experiments belong in `docs/experiments/`; raw artifacts may live under `experiments/`.

Each experiment should record:

- Hypothesis
- Question
- Method
- Inputs
- Environment/equipment, when relevant
- Results
- Interpretation
- Decision
- Limitations
- Follow-up

Failed experiments and unexpected results are retained.

## Canonical data

Machine-readable files under `language/` will become the source of truth for canonical language data. Human-readable specifications explain the rules and rationale.

At v0.0, unanswered fields should remain absent, empty, or explicitly marked `not_yet_determined` according to the data model. Do not populate invented values just to make the files look complete.

## Testing philosophy

Treat stable language rules like software rules. Add tests for invariants as soon as those invariants become meaningful. Do not claim audio, recognition, collision, or usability performance until the corresponding test has actually been performed.

## Status words

Canonical entries may eventually use:

- `experimental`
- `candidate`
- `stable`
- `deprecated`
- `reserved`

These statuses describe maturity; they do not substitute for evidence.

## Versioning

Version changes represent meaningful language capability/specification milestones. Repository activity alone does not advance the language version.
