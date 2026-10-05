# EXP-002 engineering evidence and bug ledger

**Date:** 2026-10-04  
**Scope:** Documentation and experiment evidence only  
**Language authority:** `whkoerner/Chordic-Language`  
**Production integration consumer:** `whkoerner/rpa-1-rocky-pentapod`

This record preserves the engineering path from concept to benchmark to failed assumptions, revisions, integration, and real-world runtime observations. It does not redesign Chordic, change token assignments, or rewrite the preserved v0.0 history.

## Evidence labels

- **PASS** — automated or repository-verifiable evidence met the stated expectation.
- **FAIL** — a test, hypothesis, or target did not hold.
- **FIXED** — a previously demonstrated failure was corrected and rerun successfully.
- **MANUAL PASS** — a real user/runtime observation was completed manually.
- **NOT RUN** — the experiment or validation has not been performed.
- **NOT ACOUSTICALLY VERIFIED** — symbolic/computational evidence exists, but microphone/listener/human-production evidence does not.

## Verified provenance

- Chordic PR #1, **`EXP-002: benchmark and compact conversational Chordic candidate`**, merged on 2026-10-04 as commit `5259ca4e2348c319e8fd6ceda4a22dc84e259548`.
- PR #1 introduced a 61-token experimental candidate, 2/3/4-note structures, compositional grammar, a reusable 37-case benchmark corpus, a timing/collision analyzer, and automated tests.
- The merged benchmark artifacts reproduce the normal-case baseline mean **8.030 s**, candidate mean **6.794 s**, baseline max **10.875 s**, candidate max **8.400 s**, **100.0%** candidate normal cases at or below 10 s, **0** exact lexical collisions, and **0** duplicate benchmark token sequences.
- Chordic Actions run #14 passed on the final PR head `36d455c4f4ab428d574c6c884026376bbfdc821e`; merged-main run #15 passed on `5259ca4e2348c319e8fd6ceda4a22dc84e259548`.
- Rocky PR #11 merged cross-repository integration evidence. Rocky runs #42-#44 failed while the Brain-path test backend was corrected; run #45 passed on the final PR head; merged-main run #46 passed again.

## Detailed experiment / bug ledger

| Experiment/test | Hypothesis | Expected result | Actual result | Failure/bug | Root cause | Revision/fix | Rerun evidence | Status | Limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Preserve v0.0 while adding EXP-002 | A faster candidate can be evaluated without erasing the project's starting state. | New candidate and experiment artifacts coexist with v0.0 history. | EXP-002 lives under candidate/benchmark/experiment files; `docs/history/v0.0-concept.md` remains unchanged. | None. | — | Candidate was added as `0.1-experimental`, not promoted over the historical baseline. | Chordic PR #1 merged. | **PASS** | This is provenance/history evidence, not language usability evidence. |
| EXP-002 candidate structure | Reusable compact symbolic forms can reduce routine timing without simply speeding playback. | Reusable tokens, compositional rules, and shorter 2/3/4-note structures at the same timing family. | 61 reusable tokens; high-frequency 2-note forms, 3-note roots, 4-note lower-frequency/named roots; same 140 ms note / 35 ms inter-note gap / 100 ms token-boundary family and 3× multiplier. | None in structural construction. | — | Added candidate profile and benchmark analyzer. | PR #1 artifacts and tests. | **PASS** | Symbolic candidate only; no stable phonology or acoustic validation. |
| Routine normal benchmark | Compact composition should move routine normal cases into the 4–10 s target without changing Rocky's 3× timing. | Candidate mean below baseline; all 17 normal cases ≤10 s. | Baseline mean 8.030 s → candidate 6.794 s; baseline max 10.875 s → candidate 8.400 s; 17/17 candidate normal cases ≤10 s. | Baseline had one normal case over 10 s. | CT2's limited compact vocabulary and literal free-English fallback dominate unsupported text timing. | EXP-002 expands reusable concepts and uses compact compositional grammar rather than opaque sentence shortcuts. | Chordic run #15 **PASS**; Rocky PR #11 independently reproduces the 17-case baseline through Rocky's real timing path. | **PASS** | Fixed corpus; does not prove arbitrary free-conversation timing. |
| Exact lexical collision analysis | Candidate token forms should not duplicate one another exactly. | 0 exact lexical collisions. | 0 exact lexical collisions. | None. | — | Analyzer checks all candidate forms. | `test_symbolic_collision_and_ambiguity_checks` passed. | **PASS** | Exact symbolic equality is much weaker than acoustic distinguishability. |
| Benchmark sequence uniqueness | Registered benchmark meanings should not share the same token sequence. | 0 duplicate benchmark sequences. | 0 duplicate benchmark token sequences across 37 cases. | None. | — | Registry/analyzer checks token sequences and round-trip canonical English. | Chordic test and Rocky pinned-snapshot round-trip test passed. | **PASS** | Only registered benchmark intents are covered. |
| Short-form acoustic distinguishability | Symbolic edit-distance protection may translate to reliable human/microphone recognition. | Short forms remain distinguishable across voices, pitch ranges, noise, and microphones. | Not tested. Distance-1 symbolic near-neighbors remain. | Symbolic tests cannot establish acoustic recognition. | No generated-audio, microphone, listener, or human-production experiment has yet been run. | None yet; preserve risk instead of claiming recognizability. | No acoustic rerun exists. | **NOT ACOUSTICALLY VERIFIED** | Human listening, microphone recognition, pitch-range robustness, noise/reverb, and production accuracy remain separate evidence. |
| Long historical multi-clause seed `S008` | Compact composition might bring even the long historical seed near the routine timing target. | Preferably ≤10 s, without an opaque whole-sentence code. | CT2/free-English baseline 26.355 s; EXP-002 candidate 31.350 s at 3×. | Long seed remains far over the routine target and is slower under EXP-002. | Many meaningful reusable concepts and explicit boundaries are required for a multi-clause message; compositionality has real cost. | **No benchmark-gaming fix was applied.** An opaque whole-sentence shortcut was explicitly rejected. | Result remains reproducible from committed corpus/analyzer. | **FAIL** | Routine timing target is not intended to force every complex message under 10 s. |
| Chordic automated validation | The new benchmark/collision logic should coexist with the original v0.0 integrity checks. | Entire repository test discovery passes on PR and merged main. | Chordic runs #14 and #15 passed under Python 3.13 with `python -m unittest discover -s tests -v`. | None on final EXP-002 head. | — | Added five EXP-002 tests while retaining 11 v0.0 integrity tests. | Run #14 **PASS**; run #15 **PASS**. | **PASS** | These are unit/data tests, not acoustic tests. |
| Rocky Brain-path integration: first backend | A generic existing test backend would accept the benchmark `ConversationOutput`. | Benchmark utterance traverses Brain → SafetyValidator → communication task while motion stays disabled. | Rocky run #42 failed in the Conversational Brain V1 test step. | Initial backend could not correctly dispatch arbitrary `ConversationOutput`. | `SimulatorHardware` was unsuitable for this communication-path test. | Replaced it with a dedicated communication-only test backend. | Subsequent run exposed the next capability omission rather than this backend-shape issue. | **FIXED** | Cross-repo integration failure, not a Chordic-language failure. |
| Rocky Brain-path integration: text capability | Communication-only backend should satisfy SafetyValidator without gaining motion authority. | Text communication accepted; motion remains disabled. | Rocky runs #43 and #44 failed because SafetyValidator rejected the backend. | Replacement backend omitted `Capability.TEXT_COMMUNICATION`. | Capability declaration did not match the communication request. | Added `TEXT_COMMUNICATION` while retaining no motion capability. | Rocky run #45 passed all four Windows/Ubuntu × Python 3.12/3.13 cells plus Arduino; merged-main run #46 passed. | **FIXED** | Verifies architecture boundaries and capabilities, not acoustic playback. |
| Rocky pinned EXP-002 integration snapshot | Rocky can test Chordic without becoming a second language authority. | Pinned, read-only snapshot; no independent token redesign; no production hardware authority changes. | PR #11 uses a non-authoritative snapshot and verifies motion remains disabled. | None after backend fixes. | — | Chordic remains authoritative; Rocky consumes versioned/pinned export data. | Rocky run #45 and merged-main run #46 **PASS**. | **PASS** | Snapshot can become stale; provenance must remain explicit and upgrades intentional. |
| Real desktop CT2/free-English fallback after shorter personality | Making Rocky's English replies shorter/telegraphic might by itself make production playback acceptably short. | Substantially shorter real desktop playback. | User-reported approximate durations remained **14.07 s, 50.84 s, 35.06 s, and 24.32 s**. | English-style reduction alone did not remove long fallback playback. | Production still uses CT2/free-English fallback for unsupported content; EXP-002 is not the production playback representation. | No language-data change in this documentation task. The next runtime step is to wire EXP-002 or a successor into actual playback with defined fallback semantics. | Real desktop observation was completed manually; no committed machine-readable timing log currently backs these four values. | **MANUAL PASS / FAIL** | **MANUAL PASS** for observing runtime behavior; **FAIL** for the hypothesis that shorter English prose alone solves structural fallback. These values are not EXP-002 timings. |
| Acoustic/listening evaluation | Symbolic gains should survive real audio and human/microphone use. | Measured listener and recognizer performance across pitch range, noise/reverb, and human production. | Not performed. | Evidence gap. | Acoustic experiment infrastructure and protocol have not yet been executed. | Next experiment should test short distance-1 forms first, then broader candidate material. | None. | **NOT RUN / NOT ACOUSTICALLY VERIFIED** | Do not claim human recognizability from unit tests. |
| Persistent translated English speech presentation layer | English speech can remain available persistently without redefining Chordic itself. | Optional independent presentation layer can be toggled/persisted while Chordic remains the encoded language. | Not implemented/evaluated in this repository. | None yet; feature is pending. | Presentation-layer work belongs in runtime integration, not core token assignment. | Keep it separate from Chordic language semantics and acoustic validation. | None. | **NOT RUN** | English speech quality/inflection is a separate runtime concern. |

## Automated evidence inventory

The Chordic workflow runs Python 3.13 and executes:

`python -m unittest discover -s tests -v`

The repository currently contains 11 preserved v0.0 integrity tests plus these five EXP-002 tests:

1. `test_rocky_ct2_baseline_snapshot_matches_documented_examples`
2. `test_normal_conversation_meets_target_at_unchanged_three_x_speed`
3. `test_common_expressions_are_shorter`
4. `test_symbolic_collision_and_ambiguity_checks`
5. `test_registered_intents_round_trip_to_same_canonical_english`

The final PR-head Chordic workflow run #14 passed; merged-main run #15 passed.

Rocky's cross-repository PR #11 added five focused EXP-002 integration tests covering pinned provenance, reproduction of Rocky CT2 timing, candidate timing at unchanged speed, registered-intent uniqueness, and the Brain/Safety/Task communication path with motion disabled. Its failure history is intentionally retained: runs #42–#44 failed during backend correction; run #45 passed all four Windows/Ubuntu × Python 3.12/3.13 software cells and Arduino Uno compilation; merged-main run #46 passed.

## Interpretation boundary

The desktop values **14.07 / 50.84 / 35.06 / 24.32 s** are CT2/free-English fallback runtime observations. They do **not** mean EXP-002 itself took 50 seconds. They show that prose shortening does not remove the structural fallback cost when the compact candidate is not actually driving production playback.

Likewise, zero exact symbolic collisions and successful round trips do **not** mean people or microphones can recognize the forms reliably.

## Authority and integration rule

Chordic-Language is authoritative for language design. Rocky may consume pinned/versioned exports or snapshots for tests and runtime integration, but should not independently redefine Chordic tokens, grammar, or canonical language behavior.

## Unresolved questions

- Which compact forms remain reliably distinguishable when synthesized and listened to?
- How does microphone recognition change across speaker pitch ranges, noise, reverberation, and human production?
- What fallback semantics should production runtime use for concepts not covered by the current candidate?
- How should a production runtime select between compact Chordic composition and fallback without silently changing meaning?
- Which versioned export format should Rocky pin when EXP-002 or its successor becomes production playback?
- Should persistent translated English speech be on by default, and how should it remain clearly separate from Chordic timing/evidence?

## Next recommended experiment

Wire a **pinned EXP-002 (or successor) export** into a non-motion desktop playback path, define explicit fallback semantics for out-of-vocabulary concepts, then collect side-by-side timing plus generated-audio/listener/microphone evidence. Start with the known short distance-1 neighbors and routine 17-case corpus. Keep translated English speech as a separately toggled presentation layer so its persistence or voice behavior cannot be confused with Chordic's language design.
