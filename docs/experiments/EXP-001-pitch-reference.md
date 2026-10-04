# EXP-001 — Pitch Reference

**Status:** Planned  
**Language version:** v0.0 — Concept  
**Decision link:** [ADR-001 — Pitch Reference Strategy](../decisions/ADR-001-pitch-reference-strategy.md)

## Hypothesis

A representation based on relative pitch relationships or normalized contour will preserve expression identity across different base pitch ranges more reliably than a representation based on fixed absolute frequencies.

This is a hypothesis, not a current Chordic rule.

## Question being tested

How should Chordic represent tonal identity so that equivalent patterns can survive transposition while different patterns remain distinguishable?

## Method

Initial phase:

1. Define a deliberately small set of symbolic candidate tone patterns. These are experiment stimuli, not vocabulary.
2. Express each pattern at multiple base pitch ranges.
3. Compare at least these recognition strategies:
   - absolute-frequency matching
   - relative-interval matching
   - contour/rank matching
   - normalized/hybrid matching if a clear normalization method is available
4. Measure whether each strategy:
   - identifies transposed versions as equivalent
   - keeps intentionally different patterns distinct
   - creates accidental collisions
5. Preserve all stimuli, scripts, and raw results.

Later human-production phases may repeat the comparison with humming and whistling.

## Inputs

Not yet determined. Candidate patterns have not yet been selected.

## Environment or equipment

Initial symbolic/computational phase: Not yet determined.

Human/audio phase: Not yet tested and no equipment has been selected.

## Results

Not yet tested.

## Interpretation

Not yet tested.

## Decision

No pitch-reference strategy is selected at this time.

## Limitations

- A symbolic experiment cannot establish human producibility.
- Perfect synthetic pitches cannot establish microphone or noise tolerance.
- A small pattern set may underestimate collisions.
- Humming and whistling may behave differently.

## Follow-up

After the initial symbolic comparison:

- decide whether one or more strategies deserve audio synthesis trials
- design human-production trials only after stimuli and scoring are defined
- create a new ADR if evidence supports a canonical v0.1 pitch representation
