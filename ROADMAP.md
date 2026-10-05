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

- EXP-002 is the active compact symbolic conversational candidate: 61 reusable tokens, a 37-case benchmark, and 17/17 normal cases at or below 10 seconds at Rocky's unchanged 3× timing.
- Run EXP-001 / acoustic follow-up work to determine whether the shortest candidate forms are human- and machine-distinguishable across pitch ranges.
- Test the known distance-1 short-form neighbors with generated audio, microphones, and listeners.
- Preserve explicit token boundaries unless recognition evidence supports a safer/faster alternative.
- Keep Chordic-Language authoritative; Rocky should consume pinned/versioned exports or snapshots instead of redefining Chordic independently.

## Next

- Wire EXP-002 or a successor into production desktop playback through a pinned/versioned Chordic export; do not treat current CT2/free-English fallback timing as EXP-002 timing.
- Define explicit fallback semantics for concepts outside the current compact candidate and measure fallback frequency in real conversation.
- Run actual acoustic/listening evaluation across microphones, pitch ranges, noise/reverberation, and human production; symbolic collision tests are not sufficient.
- Evaluate optional persistent translated English speech as a separate presentation layer rather than part of Chordic's core encoding.
- Decide whether relative pitch, contour, normalization, another strategy, or a hybrid should replace the current synthesis-only pitch mapping based on acoustic evidence.
- Reassign or lengthen short forms that fail listener/microphone distinction tests.
- Extend comparison/quantity grammar needed by remaining unsupported seed concepts.
- Add multi-turn context-omission experiments without enabling omission in production prematurely.
- Promote a stable language version only after both timing and acoustic distinguishability have evidence.

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
