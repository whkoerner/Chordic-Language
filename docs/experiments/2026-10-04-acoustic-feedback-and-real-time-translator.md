# Acoustic feedback and real-time translator direction — 2026-10-04

This note records operator feedback from the first merged Rocky desktop implementation that could audibly play Chordic and spoken-English translation on Windows.

It does **not** change EXP-002 vocabulary, grammar, token IDs, pitch mappings, or benchmark semantics. Those remain governed by the existing candidate/specification artifacts.

## Operator-observed evidence

The operator reports that:

- Chordic pitches were clearly audible;
- spoken-English translation was clearly audible;
- multi-turn translated conversation worked;
- replay worked;
- speed multipliers 2x and 1x were exercised;
- the supplied transcript displayed CT2, so these observations are not evidence that EXP-002 free-form timing has passed;
- the pure tonal rendering still sounds too robotic;
- the desired species-communication character is more biological, resonant, vibrational, and somewhat whale-like;
- the human translation voice also needs tuning;
- for the current desktop experience, spoken English should overlap the Chordic output rather than waiting for it to finish.

## Acoustic design direction

Chordic should sound as if it evolved as a species communication system, not as a sequence of computer beeps.

Desired qualities:

- strong, stable pitch identity for recognition;
- resonance and harmonic body;
- subtle vibration or modulation;
- smoother attack and release;
- musical continuity;
- organic phrasing;
- clearly distinguishable token boundaries;
- low enough acoustic ambiguity for software recognition.

Potential experiments should change **timbre**, not silently redefine semantics. Candidate dimensions include:

- vibrato depth and rate;
- harmonic mix;
- amplitude pulsing;
- attack/release envelope;
- glide/portamento;
- resonance;
- token-boundary rhythm.

Every candidate should remain A/B comparable against a pure-tone reference.

## Recognition constraint

A more organic sound is not automatically better. Any acoustic renderer must preserve the properties a recognizer needs.

Future evaluation should measure separately:

1. human preference;
2. token recognizability;
3. pitch-confusion rate;
4. timing/latency;
5. noise tolerance;
6. microphone robustness.

Do not call an acoustic candidate "natural", "whale-like", or "better" from unit tests alone. Those are subjective listening claims.

## Real-time translator direction

Longer-term goal: a phone or computer should be able to hear Chordic, recognize it incrementally, and translate it quickly enough to feel like live conversation.

The target architecture should eventually support:

- streaming microphone input;
- token-boundary detection before the whole utterance ends;
- incremental semantic decoding;
- partial translation as recognized tokens arrive;
- optional spoken-English rendering;
- low-latency response generation;
- laptop/phone deployment before robot hardware integration.

Latency should be measured as separate stages:

- acoustic capture;
- recognition;
- semantic decode;
- translation;
- English synthesis;
- total end-to-end wall time.

This future architecture strongly favors compact semantic tokens over spelling arbitrary English through tonal fallback.

## Relationship to Rocky

Rocky is one runtime/test client for Chordic. Rocky may experiment with rendering styles, but it must not become a second source of truth for Chordic vocabulary or grammar.

The current Rocky follow-up branch is testing a resonant rendering mode while retaining a pure-tone reference. Results from human listening and future recognition tests should flow back here as experiment evidence before any acoustic convention is promoted into a stable Chordic specification.


## Second Windows listening session — refined acoustic requirements

A second Rocky Windows session provided more specific failures:

- the resonant candidate still sounded too robotic;
- note changes felt too fast and too much like beeps;
- desired Chordic character is lower, smoother, more continuous hum/rumble/vibration;
- English voice lacked natural question cadence, pauses, and emotional weight;
- desired translation scheduler is not simultaneous start:
  - Chordic starts first;
  - English follows roughly 0.5-1.0 seconds later;
  - Chordic should normally finish slightly before English;
  - Chordic should be slightly quieter than English so translation stays intelligible.

This reinforces that the acoustic layer needs controlled experiments in continuity and envelope shape, not merely additional harmonics on short discrete tones.

For future acoustic candidates, add explicit measures for:
- transition smoothness;
- note dwell time;
- low-frequency energy/body;
- perceived continuity between semantic units;
- relative English/Chordic loudness;
- whether the intended finish ordering is achieved.

The supplied Rocky session was still using CT2. Long fallback sequences may make the requested finish ordering impossible without either compact semantic encoding or changed timing. Do not solve that limitation by silently changing Chordic semantics.
