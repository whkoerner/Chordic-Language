# EXP-003 Rocky integration evidence

Date: 2026-10-05

This note records downstream integration evidence without changing the EXP-003 candidate data pinned at `654deaa0ab7c77efe4d36876936a73ec0890065c`.

## Downstream draft

Rocky draft PR #16, branch `feat/exp-003-runtime-consumer`, is stacked on Rocky PR #15.

It:
- pins the EXP-003 runtime export and benchmark from this Chordic branch;
- pins the Chordic-owned EXP-002 surface export;
- removes Rocky's independent hard-coded EXP-002 surface dictionary;
- adds `/language exp003`;
- reports semantic coverage/fallback telemetry;
- adds the `contour-v1` continuous renderer;
- preserves CT1/CT2/EXP-002 and Brain/Safety/hardware authority.

## CI evidence

Rocky Actions run #81 at `dc1729b0644ed9b5b5ddbd888173dde5747180f9` passed:
- Ubuntu Python 3.12;
- Ubuntu Python 3.13;
- Windows Python 3.12;
- Windows Python 3.13;
- Arduino Uno compilation.

The green run followed preserved failed runs #76-#80. The failure sequence exposed generated-edit syntax defects and then a missing `contour-v1` PCM dispatch allowlist; those failures and fixes are documented in Rocky's EXP-003 integration test plan.

## What this does and does not establish

Automated integration establishes:
- deterministic semantic parsing;
- exact English round-trip;
- compositional arithmetic;
- no fallback for the current real math and food/energy/build samples;
- explicit fallback for unseen lexical concepts;
- modelled timing reproduction;
- deterministic/bounded contour PCM generation;
- cross-platform software compatibility.

It does **not** establish:
- natural/alien/whale-like subjective sound;
- human vocal reproducibility;
- microphone recognition;
- noisy-room recognition;
- streaming acoustic recognition latency.

Those remain manual/future experiments.
