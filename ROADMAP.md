# Chordic Language Roadmap

This roadmap tracks demonstrated capability, not just files or code written. A task is not complete until its relevant acceptance criteria or evidence are satisfied.

## Completed

- Repository created.
- Project identity established as Chordic Language / Chordic.
- Experimental language baseline established at v0.0 — Concept.
- Evidence-first and history-preservation principles established.
- Split software/content licensing established.
- Minimum v0.0 machine-readable data model created without inventing language rules.
- All 11 required seed expressions preserved as unsupported future acceptance targets.
- Initial automated language-data validation added and passed in GitHub Actions.
- ADR-001 records that the pitch-reference strategy is intentionally undecided.
- EXP-001 defines the first planned pitch-reference comparison.

## Current

- Select a deliberately small set of non-language experimental tone patterns for EXP-001.
- Define the scoring and collision criteria for EXP-001 before collecting results.
- Run EXP-001 and preserve stimuli, scripts, raw results, and interpretation.

## Next

- Decide whether relative pitch, contour, normalization, another strategy, or a hybrid should advance to a candidate representation based on evidence.
- Define only the smallest sound inventory supported by evidence.
- Add collision and legality tests as soon as canonical tonal forms exist.
- Define the first primitive concepts only after a usable representation exists.
- Consider v0.1 only when a tested sound inventory and initial primitive concepts actually exist.

## Later / research

The following are directional milestones, not promises or automatic version bumps:

- v0.1 — sound inventory and primitive concepts
- v0.2 — basic grammar and dictionary
- v0.3 — audio synthesis
- v0.4 — generated-audio recognition
- v0.5 — human-produced sound recognition
- v0.6 — bidirectional translation
- v0.7 — noise and error-resistance testing
- v0.8 — robot integration
- v0.9 — human learning and usability trials
- v1.0 — stable specification

Research topics include humming, whistling, timing tolerance, speaker pitch differences, microphone variation, noise, reverberation, pitch drift, confidence, false positives, tonal collisions, learnability, fatigue, and gesture integration.

## Version advancement rule

Do not advance the language merely because implementation work occurred. A version milestone should correspond to a meaningful, documented capability/specification change supported by appropriate tests or experiments.
