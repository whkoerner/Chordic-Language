# EXP-004 natural-carrier trajectory v0

Date: 2026-10-05

Status: **acoustic experiment only — not promoted to the runtime language**

Source semantic export: `EXP-003-runtime-v3`

## Why this experiment exists

EXP-003 v0.3 established the preferred semantic/timing system and the in-process `vocal-v1` renderer direction. Manual Windows feedback said the lower register and speed were much closer to the desired result, but the sound still felt too robotic.

The next experiment therefore changes **carrier planning only**.

It does not change:

- token IDs;
- contour codes;
- grammar;
- semantic surface mappings;
- number composition;
- token duration classes;
- default duration multiplier;
- fallback behavior.

## Target sound

The subjective target remains:

**natural low rumble / low-register tonal bird call / alien-animal-like vocalization**

Avoid:

- whistle;
- alarm;
- sterile sine tone;
- MIDI-note character;
- bright chirp;
- abrupt pitch resets.

No automated test can prove this subjective target was achieved. Listening remains NOT RUN.

## What EXP-004 adds

`tools/exp004_carrier_plan.py` converts fully semantic EXP-003 text into a renderer-neutral frame plan.

Each frame records:

- start time;
- frame duration;
- F0;
- amplitude;
- voiced/unvoiced state;
- owning semantic token;
- contour phase;
- deterministic micro-pitch variation.

Each token record also preserves the original EXP-003 contour code and its four target frequencies.

This gives future renderers a single deterministic source of F0/timing truth.

## Continuous vocal trajectory

The planner uses log-frequency smoothstep interpolation between semantic targets instead of independent note events.

Token boundaries remain voiced and use an amplitude dip rather than a full stop.

The pitch code remains speaker-relative:

- baseline: existing EXP-003 120 Hz reference;
- semantic offsets: existing -4, -2, 0, +2, +4 semitone degrees;
- deterministic microvariation: maximum 0.08 semitone.

The microvariation is intentionally much smaller than the 2-semitone semantic pitch spacing.

## Renderer-neutral carrier hints

The plan includes experimental hints rather than hard-coded semantics:

- formant hints around 340 / 880 / 1480 Hz;
- restrained subharmonic mix;
- low breathiness;
- phrase pulse around 1.6 Hz.

These are not language symbols. A future renderer may ignore or tune them while preserving the F0/semantic trajectory.

## Offline vocoder candidates

The intended next A/B experiments are:

### WORLD / PyWORLD

Use a natural low vocal carrier, estimate spectral envelope/aperiodicity, replace or transform F0 with the EXP-004 trajectory, then resynthesize locally.

Useful properties to verify before promotion:

- Windows installation;
- deterministic output;
- offline operation;
- latency;
- licensing;
- whether F0 manipulation preserves the intended low organic carrier;
- whether semantic contours remain distinguishable.

### Praat / Parselmouth

Use Praat manipulation through Parselmouth for pitch/formant experiments against a recorded or synthetic low vocal carrier.

Again, this is an experimental sidecar candidate rather than a required runtime dependency.

## Benchmark

`benchmarks/exp-004-natural-carrier-plan-v0.json` contains fully semantic production-like phrases.

Automated requirements:

- 100% semantic coverage;
- zero fallback;
- same semantic token codes as EXP-003;
- same total duration as EXP-003 timing;
- F0 remains in the existing low 80–180 Hz target band;
- microvariation remains <= 0.08 semitone;
- token boundaries remain voiced;
- deterministic output.

Subjective requirements remain NOT RUN until a human listens.

## Promotion gate

Do not replace `vocal-v1` merely because EXP-004's trajectory tests pass.

Promotion requires at minimum:

1. actual audio rendered from at least two carrier backends;
2. human A/B listening against `vocal-v1`;
3. no semantic/timing regression;
4. no bright chirp/alarm failure;
5. acceptable Windows latency;
6. offline operation after provisioning;
7. dependency/license documentation;
8. recognition-distance checks after any F0/formant processing.

Until then, EXP-004 remains a reproducible acoustic experiment only.
