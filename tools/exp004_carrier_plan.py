"""EXP-004 natural-carrier trajectory experiment.

This experiment does not change EXP-003 semantics. It converts the existing
relative-pitch contour tokens into a renderer-neutral, smoothly sampled F0 and
amplitude plan suitable for later WORLD/PyWORLD/Parselmouth experiments.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from tools.exp003_v2_benchmark import parse_text


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "language" / "runtime" / "exp-003-runtime-export-v3.json"
PROFILE_ID = "EXP-004-natural-carrier-plan-v0"
FRAME_MS = 10.0
MAX_MICRO_JITTER_SEMITONES = 0.08


def load_runtime():
    return json.loads(RUNTIME.read_text(encoding="utf-8"))


def _hz(baseline, semitones):
    return baseline * 2 ** (semitones / 12.0)


def _smoothstep(value):
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def _interp_log_hz(first, second, t):
    if first <= 0 or second <= 0:
        raise ValueError("F0 must stay positive")
    a = math.log2(first)
    b = math.log2(second)
    return 2 ** (a + (b - a) * _smoothstep(t))


def _micro_semitones(token_index, frame_index):
    # Deterministic low-amplitude quasi-organic microvariation. It remains far
    # below the 2-semitone code spacing and is metadata-visible for recognition.
    phase = token_index * 1.713 + frame_index * 0.417
    return MAX_MICRO_JITTER_SEMITONES * (
        0.67 * math.sin(phase) + 0.33 * math.sin(phase * 0.381 + 0.9)
    )


def _append_segment(frames, *, duration_ms, start_hz, end_hz, amp_start, amp_end,
                    token, segment, token_index, start_ms):
    if duration_ms < 0:
        raise ValueError("negative carrier duration")
    remaining = float(duration_ms)
    frame_index = 0
    cursor = float(start_ms)
    while remaining > 1e-9:
        width = min(FRAME_MS, remaining)
        midpoint = (duration_ms - remaining + width / 2.0) / max(duration_ms, 1e-9)
        base_hz = _interp_log_hz(start_hz, end_hz, midpoint)
        jitter = _micro_semitones(token_index, frame_index)
        f0 = _hz(base_hz, jitter)
        amp = amp_start + (amp_end - amp_start) * _smoothstep(midpoint)
        frames.append(
            {
                "start_ms": round(cursor, 3),
                "duration_ms": round(width, 3),
                "f0_hz": round(f0, 4),
                "amplitude": round(max(0.0, min(1.0, amp)), 4),
                "voiced": True,
                "token": token,
                "segment": segment,
                "micro_jitter_semitones": round(jitter, 5),
            }
        )
        cursor += width
        remaining -= width
        frame_index += 1
    return cursor


def carrier_plan(tokens, runtime=None, *, multiplier=None):
    runtime = runtime or load_runtime()
    candidate = runtime["candidate"]
    acoustics = candidate["acoustics"]
    timing = acoustics["timing_ms"]
    multiplier = (
        acoustics["default_duration_multiplier"] if multiplier is None else multiplier
    )
    if type(multiplier) not in (int, float) or not 1 <= float(multiplier) <= 6:
        raise ValueError("multiplier must be between 1 and 6")
    multiplier = float(multiplier)

    registry = {row["id"]: row for row in candidate["tokens"]}
    patterns = {
        row["id"]: tuple(row["contour_code"]) for row in candidate["tokens"]
    }
    offsets = {
        int(key): float(value)
        for key, value in acoustics["pitch_offsets_semitones"].items()
    }
    baseline = float(acoustics["reference_baseline_hz"])
    frames = []
    token_rows = []
    cursor = 0.0
    previous_hz = baseline

    # Header/profile marker are still voiced carrier events, not isolated beeps.
    cursor = _append_segment(
        frames,
        duration_ms=timing["phrase_header"] * multiplier,
        start_hz=baseline,
        end_hz=_hz(baseline, -1.0),
        amp_start=0.15,
        amp_end=0.55,
        token="__PHRASE__",
        segment="phrase_header",
        token_index=0,
        start_ms=cursor,
    )
    cursor = _append_segment(
        frames,
        duration_ms=timing["profile_marker"] * multiplier,
        start_hz=_hz(baseline, -1.0),
        end_hz=baseline,
        amp_start=0.55,
        amp_end=0.62,
        token="__PROFILE__",
        segment="profile_marker",
        token_index=0,
        start_ms=cursor,
    )
    previous_hz = baseline

    for token_index, token in enumerate(tokens, start=1):
        if token not in registry:
            raise ValueError(f"unknown EXP-003 token: {token}")
        row = registry[token]
        gesture_ms = (
            timing["short_gesture"]
            if row["duration_class"] == "short"
            else timing["root_gesture"]
        ) * multiplier
        degrees = patterns[token]
        targets = tuple(_hz(baseline, offsets[degree]) for degree in degrees)
        token_start = cursor

        # Four semantic pitch targets are reached through four smooth phases.
        phase_ms = gesture_ms / len(targets)
        source_hz = previous_hz
        for anchor_index, target_hz in enumerate(targets):
            cursor = _append_segment(
                frames,
                duration_ms=phase_ms,
                start_hz=source_hz,
                end_hz=target_hz,
                amp_start=0.66 if anchor_index else 0.54,
                amp_end=0.68,
                token=token,
                segment=f"anchor_{anchor_index}",
                token_index=token_index,
                start_ms=cursor,
            )
            source_hz = target_hz

        boundary_ms = timing["token_boundary"] * multiplier
        cursor = _append_segment(
            frames,
            duration_ms=boundary_ms,
            start_hz=source_hz,
            end_hz=source_hz,
            amp_start=0.50,
            amp_end=0.26,
            token=token,
            segment="token_boundary",
            token_index=token_index,
            start_ms=cursor,
        )
        previous_hz = source_hz
        token_rows.append(
            {
                "token": token,
                "duration_class": row["duration_class"],
                "contour_code": list(degrees),
                "target_hz": [round(value, 4) for value in targets],
                "start_ms": round(token_start, 3),
                "end_ms": round(cursor, 3),
            }
        )

    f0_values = [frame["f0_hz"] for frame in frames]
    jitter_values = [abs(frame["micro_jitter_semitones"]) for frame in frames]
    return {
        "schema_version": 1,
        "experiment": PROFILE_ID,
        "source_export": runtime["export_id"],
        "semantic_source": runtime["candidate_id"],
        "multiplier": multiplier,
        "frame_ms": FRAME_MS,
        "carrier": {
            "kind": "renderer-neutral-natural-vocal-trajectory",
            "baseline_hz": baseline,
            "formant_hint_hz": [340, 880, 1480],
            "subharmonic_mix_hint": 0.16,
            "breathiness_hint": 0.06,
            "amplitude_pulse_hz_hint": 1.6,
            "naturalness_status": "NOT_RUN_REQUIRES_HUMAN_LISTENING",
        },
        "tokens": token_rows,
        "frames": frames,
        "metrics": {
            "total_duration_seconds": round(cursor / 1000.0, 3),
            "min_f0_hz": round(min(f0_values), 3) if f0_values else None,
            "max_f0_hz": round(max(f0_values), 3) if f0_values else None,
            "max_abs_micro_jitter_semitones": round(
                max(jitter_values), 5
            ) if jitter_values else 0.0,
            "semantic_token_count": len(tokens),
        },
    }


def plan_text(text, runtime=None, *, multiplier=None):
    runtime = runtime or load_runtime()
    parsed = parse_text(text, runtime)
    if parsed["fallback_spans"]:
        raise ValueError(
            "EXP-004 carrier-plan experiment requires fully semantic EXP-003 text"
        )
    result = carrier_plan(parsed["tokens"], runtime, multiplier=multiplier)
    result["english"] = text
    result["semantic_coverage_percent"] = parsed["semantic_coverage_percent"]
    return result


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--multiplier", type=float)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    plan = plan_text(args.text, multiplier=args.multiplier)
    raw = json.dumps(plan, indent=2) + "\n"
    if args.output:
        args.output.write_text(raw, encoding="utf-8")
    else:
        print(raw, end="")


if __name__ == "__main__":
    main()
