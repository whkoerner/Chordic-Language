# EXP-002 real Rocky free-form baseline — 2026-10-04

Status: manual runtime evidence, not a language release.

## Why this evidence matters

The first Windows sessions that showed 22–25 second Chordic replies were running CT2. A later session explicitly switched Rocky to EXP-002, allowing the first direct production-style free-form comparison.

## EXP-002 runtime samples

Prompt:
what is 8 times 8?

Rocky reply:
8 times 8 is 64. Rocky calculate. Good.

Measured:
- EXP-002 reported active
- Chordic: 20.48 s
- English: 6.77 s
- Chordic outlasted English by 12.96 s

Prompt:
what is your favorite food?

Rocky reply:
Rocky no eat. Rocky think food is energy. Rocky use energy to think and build.

Measured:
- EXP-002 reported active
- Chordic: 36.41 s
- English: 8.38 s
- Chordic outlasted English by 27.28 s
- Rocky warned that fallback was exact but not fluent speech

## Interpretation

These real free-form results do not contradict the published EXP-002 registered-case benchmark.

The existing benchmark demonstrates that supported compact semantic sequences can meet the routine timing goal.

The production Rocky adapter still lacks ordinary mappings for concepts used in these examples, including math/numeric material and food/eat/energy/build vocabulary. Unsupported spans are carried through exact fallback, which dominates duration.

The benchmark corpus itself does not currently exercise these domains.

Therefore EXP-002 has demonstrated compactness for its covered semantics, but has not demonstrated sufficient coverage for open-ended conversation.

## New requirement for successor work

Future EXP-003 evaluation must publish both:
1. timing for fully supported semantic sequences;
2. real free-form coverage/fallback metrics.

At minimum measure:
- semantic token count;
- unsupported span count;
- fallback bytes;
- fallback percentage;
- duration caused by semantic encoding;
- duration caused by fallback;
- total duration.

Add real conversational domains such as:
- arithmetic/numbers;
- food/preferences;
- names;
- common objects/actions;
- technical explanation;
- social conversation.

## Authority implication

Rocky's current hard-coded English-surface mapping is integration code, not an appropriate long-term source of language truth.

Future candidate surface mappings, semantic lexicon, grammar, and runtime export data should live in Chordic-Language and be versioned here. Rocky should consume the export.

## Decision

Keep EXP-002 unchanged as historical evidence.

Use these production results as baseline evidence motivating EXP-003 or another successor with:
- broader semantic coverage;
- far less literal fallback;
- compact composition;
- human-vocalizable continuous acoustics;
- future streaming recognition suitability.
