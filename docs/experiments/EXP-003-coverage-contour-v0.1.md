# EXP-003 coverage-first continuous contour candidate

Status: experimental candidate. Human listening, human vocal production, microphone recognition, and streaming recognition are **NOT RUN**.

## Evidence that motivated the experiment

The first real Rocky EXP-002 free-form session produced:

- `8 times 8 is 64. Rocky calculate. Good.`: 20.48 s Chordic versus 6.77 s English.
- `Rocky no eat. Rocky think food is energy. Rocky use energy to think and build.`: 36.41 s Chordic versus 8.38 s English.

Those timings do not show that compact EXP-002 semantic tokens require 20-36 seconds. Inspection of Rocky's runtime adapter showed that its local surface registry lacked ordinary math/numeric and food/eat/energy/build mappings. Exact CT2/UTF-8 fallback therefore dominated the production replies.

EXP-003 is justified as a coverage-first successor experiment. Timing and semantic coverage are measured together for every benchmark row.

## Authority architecture

Chordic-Language now owns candidate semantics and runtime surface data:

```
Chordic-Language
  language/candidates/exp-003-contour-v0.1.json
  language/runtime/exp-003-runtime-export.json
  language/runtime/exp-002-runtime-export.json
  benchmarks/exp-003-open-conversation.json
        |
        v
Rocky pinned runtime copy / deterministic adapter
```

The EXP-002 surface export is intentionally separate from the historical candidate file. It preserves the exact semantic surface registry that had been manually maintained in Rocky so that Rocky can migrate away from its hard-coded `_SURFACES` dictionary without rewriting EXP-002 history.

## Semantic structure

EXP-003 v0.1 has 106 reusable semantic tokens. It expands coverage for:

- digits 0-9 and compositional decimal quantities;
- multiplication/addition/subtraction/division;
- equality;
- food/eat/energy;
- preferences and color;
- common actions including use/build/calculate/measure;
- thinking/learning/knowing/remembering;
- names and relationships;
- common technical conversation.

There are no whole-sentence IDs. For example:

`8 times 8 is 64`

is represented compositionally as:

`NUM.8 OP.MUL NUM.8 NUM.6 NUM.4`

Low-information English glue words such as articles, copulas, and auxiliaries may be omitted under explicit grammar rules. Unknown lexical concepts still become explicit fallback spans and are counted.

## Acoustic candidate: contour-v1

Each semantic token is one connected four-anchor contour gesture rather than four isolated note packets.

Pitch is speaker-relative, using five normalized levels around the speaker/synthesizer baseline:

`-4, -2, 0, +2, +4 semitones`

The selected symbolic family is q=5 length-4 single parity:

`(a, b, c, -a-b-c mod 5)`

For the assigned 106 tokens:

- exact collisions: 0;
- minimum Hamming distance: 2;
- minimum summed anchor-separation proxy: 4 semitones.

A 45 ms amplitude dip is the proposed token boundary cue. Within each token, pitch should glide continuously between anchors instead of playing NOTE-gap-NOTE packets.

### Human-range simulation

The same relative pattern can be produced in different absolute registers:

| speaker baseline | minimum | maximum | total span |
| ---: | ---: | ---: | ---: |
| 110 Hz | 87.3 Hz | 138.6 Hz | 8 semitones |
| 180 Hz | 142.9 Hz | 226.8 Hz | 8 semitones |
| 260 Hz | 206.4 Hz | 327.6 Hz | 8 semitones |

At the current deliberately slow 3x learning/benchmark timing, the fastest token class has a worst-case 8-semitone segment slope proxy of about 61.5 semitones/second. This is computational feasibility only, not proof that a normal person can reproduce it comfortably.

## Acoustic alternatives compared

| candidate | non-seed mean | non-seed max | slope proxy | decision |
| --- | ---: | ---: | ---: | --- |
| four discrete note packets | 13.330 s | 30.855 s | n/a | rejected: slow and preserves beep-like packets |
| contour-fast | 3.858 s | 8.325 s | 80.0 st/s | rejected for now: less production margin |
| **contour-v1** | **4.441 s** | **9.825 s** | **61.5 st/s** | selected for A/B integration |
| contour-slow | 5.025 s | 11.325 s | 50.0 st/s | rejected for now: exceeds routine 10 s target |

The selection is provisional. Automated tests cannot establish that the sound is natural, whale-like, purr-like, or pleasant.

## Coverage + timing benchmark

The corpus includes:

- hello/name exchange;
- real arithmetic response;
- favorite-color discussion;
- chicken Alfredo preference question;
- yes/no;
- a question;
- reassurance;
- technical explanation;
- the real food/energy/build response;
- a food-preference question;
- all historical seed phrases.

Every row stores:

- semantic token count;
- unsupported spans;
- fallback span count;
- fallback bytes;
- semantic coverage percent;
- fallback percent;
- semantic-token duration;
- fallback duration;
- total duration.

At unchanged 3x timing, the 11 non-seed open-conversation samples currently simulate:

- mean: **4.441 s**;
- median: **4.185 s**;
- max: **9.825 s**;
- over 10 s: **0**;
- mean semantic coverage: **100.0%**;
- fallback spans: **0**;
- fallback bytes: **0**.

All 19 samples including historical seeds simulate:

- mean: **4.176 s**;
- max: **9.825 s**;
- mean semantic coverage: **100.0%**.

These are deterministic modelled durations, not Windows acoustic wall-time measurements.

## Coverage honesty check

The runtime parser is also tested against an unseen phrase:

`Rocky calibrate spectrometer`

Only `Rocky` is semantic. `calibrate` and `spectrometer` remain explicit fallback spans. This prevents benchmark success from hiding unsupported open vocabulary.

## Recognition-oriented design

The candidate is intended to support future incremental recognition:

1. estimate speaker baseline;
2. follow relative pitch contour;
3. detect the amplitude-dip token boundary;
4. quantize four relative anchors;
5. validate parity/error distance;
6. emit a semantic token;
7. incrementally translate before the full utterance is finished.

No microphone implementation exists yet. Claims are limited to symbolic collision tests, relative pitch range simulation, and acoustic-separation proxies.

## Required Rocky migration

Rocky should next:

1. vendor/pin the Chordic runtime exports;
2. remove the independent hard-coded EXP-002 `_SURFACES` registry;
3. add `/language exp003`;
4. report semantic coverage/fallback telemetry for EXP-003 playback;
5. add a `contour-v1` renderer alongside `pure` and `resonant` for A/B testing;
6. preserve CT2 compatibility and all Brain/Safety/hardware-authority boundaries.

## NOT RUN

- actual Windows contour-v1 playback;
- subjective pure/resonant/contour-v1 listening comparison;
- human humming/voicing reproduction;
- microphone recognition;
- recognition in noise;
- streaming translator latency;
- final Chordic-vs-English relative-volume acceptance;
- final 0.5-1.0 s English lead-in acceptance.
