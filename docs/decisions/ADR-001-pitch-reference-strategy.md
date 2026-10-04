# ADR-001 — Pitch Reference Strategy

**Status:** Deferred pending experiment  
**Date:** 2026-10-04  
**Language version:** v0.0 — Concept  
**Related experiment:** [EXP-001 — Pitch Reference](../experiments/EXP-001-pitch-reference.md)

## Context

Chordic is intended to be producible by people with different vocal ranges and by machines. Equivalent expressions should ideally remain equivalent when produced by a low voice, a high voice, humming, whistling, or synthesis.

The project has not yet established whether meaning should depend on absolute frequencies, relative intervals, pitch contours/ranks, normalization, or a hybrid representation.

## Problem

A tonal representation must eventually answer a basic question:

> Which acoustic changes preserve the identity of a Chordic form?

Locking this down too early could make the language difficult for humans to produce or difficult for software to recognize.

## Options considered

### 1. Absolute frequencies or musical notes

A canonical form could require specific frequencies or named notes.

Potential advantages:

- simple to synthesize exactly
- straightforward symbolic notation

Potential problems:

- likely sensitive to speaker vocal range
- difficult for untrained humans without pitch reference
- may confuse musical notation with language identity

### 2. Relative pitch intervals

A form could be defined by changes relative to a local baseline or preceding tone.

Potential advantages:

- naturally supports transposition
- may tolerate different speaker ranges

Potential problems:

- interval production may be difficult for humans
- recognition needs a robust reference/baseline
- pitch drift could accumulate

### 3. Pitch contour or ranked levels

A form could encode relationships such as low → high → mid rather than precise intervals.

Potential advantages:

- potentially easier for humans
- potentially tolerant of range differences

Potential problems:

- lower information density
- more collisions may occur
- category boundaries must be learned and recognized reliably

### 4. Normalized or hybrid representation

Recognition could normalize a speaker's pitch range, while canonical forms combine contour, interval, duration, rhythm, or other features.

Potential advantages:

- may balance robustness and expressiveness

Potential problems:

- more complexity
- normalization assumptions could fail for short utterances or unusual production

## Decision

**Not yet determined.**

At v0.0, Chordic will not define canonical words using absolute musical notes, fixed frequencies, relative intervals, or contour categories.

The repository will first compare candidate pitch-reference strategies through EXP-001 and later experiments. A future ADR must make or supersede this decision when evidence exists.

## Reason

Cross-speaker tolerance is a project goal, but that goal alone does not prove which pitch representation works best. The decision needs evidence about distinguishability, transposition tolerance, collision risk, recognition simplicity, and eventual human production.

## Consequences

- `language/phonology.json` keeps `pitch_reference` as `not_yet_determined`.
- No canonical tonal vocabulary may depend on a pitch-reference scheme yet.
- Early tooling should avoid assuming named musical notes are semantically canonical.
- v0.1 should not be declared until a defensible initial sound representation exists.

## Evidence

Not yet tested.

See EXP-001 for the first planned comparison.
