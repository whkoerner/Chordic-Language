# EXP-002 — Compact conversational speed profile

**Date:** 2026-10-04  
**Status:** Accepted as an experimental symbolic candidate; acoustic validation still required  
**Candidate:** `0.1-experimental`  
**Rocky baseline:** `whkoerner/rpa-1-rocky-pentapod@fceb7fe8cbcc5b42d3db0e208f6a323f79e2670a`

## Question

Can Chordic represent routine conversational meaning in roughly 4–10 seconds at Rocky's existing 3× learning-speed timing without merely speeding playback up?

## Baseline and diagnosis

Rocky CT2 has 15 compact lexical entries. Unsupported English is encoded byte-by-byte as UTF-8 fallback. EXP-002 freezes the actual CT2 timing constants and starter vocabulary from Rocky so the benchmark is rerunnable. The analyzer reproduces two existing timing examples exactly:

- `hello robot` → 3.165 s at 1×
- 384 unsupported ASCII `x` characters → 31.570 s at 1×

The structural causes of slowness are therefore mostly vocabulary coverage, five-note lexical cores for every learned word, and literal English fallback—not simply playback speed.

## Candidate changes

The candidate keeps the existing five symbolic scale degrees and the same 140 ms note / 35 ms inter-note gap / 100 ms token-boundary timing family. It changes the language structure:

- two-note forms for high-frequency grammar, pronouns, and yes/no;
- three-note parity-code roots for high-frequency lexical concepts;
- four-note parity-code roots for lower-frequency/named concepts;
- unmarked present/default tense;
- omitted English-style copula for quality/state predicates;
- compact explicit markers for question, negation, past, future, command, intensity, and recommendation;
- subject/object pronoun reuse;
- omission of English infinitive `to` when the relation is unambiguous;
- explicit token boundaries retained to avoid segmentation ambiguity.

No timing multiplier was reduced.

## Measured results at Rocky 3×

| Metric | CT2 baseline | EXP-002 candidate |
| --- | ---: | ---: |
| Normal cases | 17 | 17 |
| Mean normal duration | 8.030 s | **6.794 s** |
| Median normal duration | 7.275 s | **6.525 s** |
| Maximum normal duration | 10.875 s | **8.400 s** |
| Normal cases ≤10 s | 94.1% | **100.0%** |
| Normal cases >10 s | 1 | **0** |
| Mean very-common duration | 4.421 s | **3.738 s** |

The routine target is met for all 17 normal cases at the deliberately slow 3× learning speed.

## Semantic and ambiguity checks

- 61 reusable candidate tokens.
- 0 exact lexical-form collisions.
- 0 duplicate benchmark token sequences.
- 0 framed prefix ambiguities because explicit token boundaries remain.
- Safety/meaning-critical pairs such as yes/no, question/negation, I/you, this/that, past/future, stop/go, help/wait, and come/go have symbolic edit distance at least 2.
- Every registered benchmark intent maps back to the same canonical English intent.

Short two-note forms still create many distance-1 symbolic neighbors. This is recorded as an unresolved risk. These tests are **symbolic/computational only** and do not establish microphone or human recognition.

## Seed results and failed tradeoff

The short historical Rocky-style semantic seeds now have compositional candidate token sequences where the required concepts exist. The long multi-clause crew/death/rescue-style seed remains over 20 seconds at 3× and is slightly slower than CT2 fallback in this experiment. That result is retained rather than hidden: long complex communication is allowed to exceed the routine threshold, and an opaque whole-sentence shortcut would damage compositionality and learnability.

## Rejected ideas

- Merely reduce the duration multiplier — rejected as the primary solution.
- Assign one code per benchmark sentence — rejected as benchmark gaming.
- Remove token boundaries now — rejected because it trades timing for segmentation risk before acoustic tests exist.
- Treat symbolic edit distance as acoustic validation — rejected.
- Give the complex historical seed an opaque shortcut — rejected.

## Reproduce

```bash
python -m unittest discover -s tests -v
```

The new `test_exp002.py` imports `tools.exp002_benchmark`, recomputes the timing/collision analysis, and verifies the frozen Rocky CT2 examples.

## Decision

Accept EXP-002 as a **candidate experimental profile**, not a stable language release. It demonstrates a real structural speed improvement while preserving explicit grammar and honest ambiguity limitations. The next high-value experiment is generated-audio/human recognition of the shortest distance-1 forms, alongside the still-unresolved pitch-reference work from EXP-001.

## Post-merge engineering evidence — 2026-10-04

EXP-002 was merged through Chordic PR #1, **`EXP-002: benchmark and compact conversational Chordic candidate`**, as merge commit `5259ca4e2348c319e8fd6ceda4a22dc84e259548`. The merged-main Chordic validation run #15 passed.

The committed benchmark corpus and candidate data independently reproduce the published results at unchanged Rocky 3× timing:

| Metric | Rocky CT2 baseline | EXP-002 candidate |
| --- | ---: | ---: |
| Reusable candidate tokens | — | 61 |
| Benchmark cases | 37 | 37 |
| Normal cases | 17 | 17 |
| Mean normal duration | 8.030 s | **6.794 s** |
| Maximum normal duration | 10.875 s | **8.400 s** |
| Normal cases ≤10 s | 94.1% | **100.0%** |
| Exact lexical-form collisions | — | **0** |
| Duplicate benchmark token sequences | — | **0** |

These are symbolic/timing results. They are **NOT ACOUSTICALLY VERIFIED**. They do not establish human listening accuracy, microphone recognition, pitch-range robustness, noise/reverberation robustness, or human production accuracy.

The important negative result remains preserved. Benchmark seed `S008` — `Rocky watch crew die. Could not fix. Grace say Grace will die, Rocky fix.` — measured **26.355 s** through the frozen CT2/free-English baseline and **31.350 s** through the EXP-002 candidate at 3×. It was intentionally not replaced with an opaque whole-sentence token to make the benchmark look better.

### Cross-repository Rocky integration evidence

Rocky PR #11, `Test Chordic EXP-002 through Rocky timing and Brain boundary`, merged EXP-002 as a pinned, read-only integration snapshot. This is **cross-repository integration evidence, not a Chordic-language failure**.

The integration exposed useful architecture/test failures:

- Rocky Actions run #42: **FAIL** — the first Brain integration test backend used `SimulatorHardware`, which was unsuitable for arbitrary `ConversationOutput` dispatch.
- Runs #43 and #44: **FAIL** — the replacement communication-only backend omitted `Capability.TEXT_COMMUNICATION`; `SafetyValidator` correctly rejected the conversational utterance.
- The corrected backend declared text communication while retaining **no motion capability**.
- Rocky Actions run #45: **PASS** — Windows and Ubuntu, Python 3.12 and 3.13, plus Arduino Uno compilation passed.
- Rocky merged-main run #46: **PASS**.

No production Brain, SafetyValidator, hardware, CT1/CT2, launcher, or audio behavior was changed by that integration test work.

### Real desktop observation: CT2/free-English fallback remained long

After Rocky's personality was shortened and made more telegraphic, a real desktop session still produced long production CT2/free-English fallback playback. User-reported approximate observed durations were:

- **14.07 s**
- **50.84 s**
- **35.06 s**
- **24.32 s**

These are **MANUAL PASS** observations of current runtime behavior, not EXP-002 benchmark measurements. They **do not mean EXP-002 took 50 seconds**. The observation supports a narrower engineering conclusion: shortening English prose alone does not solve the structural fallback problem. EXP-002, or a successor compact compositional representation, still needs to be wired into actual runtime playback before production conversation can benefit from the experiment's structural timing gains.

The four desktop timings are not currently backed by a committed machine-readable timing log in this repository; they remain manual runtime evidence.

### Authority and next milestone

Chordic-Language remains authoritative for Chordic language design. Rocky should consume pinned/versioned exports or snapshots for integration and must not independently redefine Chordic token assignments or grammar.

The next experiment/runtime milestone is:

1. production desktop use of EXP-002 or a successor compact representation;
2. explicit fallback semantics for concepts outside the current candidate;
3. actual acoustic/listening evaluation, including microphones, pitch ranges, noise/reverb, and human production;
4. optional persistent translated English speech as a separate presentation layer rather than part of Chordic's core encoding.

See [the EXP-002 engineering evidence and bug ledger](../history/exp-002-engineering-evidence.md) for the detailed hypothesis/failure/fix chronology.

