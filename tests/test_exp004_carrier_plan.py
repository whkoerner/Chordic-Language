"""EXP-004 natural-carrier trajectory experiment invariants."""

import json
from pathlib import Path
import unittest

from tools.exp003_v2_benchmark import parse_text, semantic_seconds
from tools.exp004_carrier_plan import (
    MAX_MICRO_JITTER_SEMITONES,
    carrier_plan,
    load_runtime,
    plan_text,
)


ROOT=Path(__file__).resolve().parents[1]
BENCHMARK=ROOT/"benchmarks"/"exp-004-natural-carrier-plan-v0.json"


class Exp004CarrierPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runtime=load_runtime()
        cls.benchmark=json.loads(BENCHMARK.read_text(encoding="utf-8"))
        cls.candidate=cls.runtime["candidate"]

    def test_exp004_never_changes_exp003_token_codes(self):
        source={
            row["id"]:tuple(row["contour_code"])
            for row in self.candidate["tokens"]
        }
        for token,code in source.items():
            plan=carrier_plan([token],self.runtime,multiplier=2)
            self.assertEqual(tuple(plan["tokens"][0]["contour_code"]),code)

    def test_benchmark_is_fully_semantic_low_band_and_timing_identical(self):
        for case in self.benchmark["cases"]:
            with self.subTest(case=case["id"]):
                parsed=parse_text(case["english"],self.runtime)
                self.assertEqual(parsed["semantic_coverage_percent"],100.0)
                self.assertEqual(parsed["fallback_spans"],[])
                plan=plan_text(case["english"],self.runtime,multiplier=2)
                expected=semantic_seconds(parsed["tokens"],self.candidate,2)
                self.assertEqual(plan["metrics"]["total_duration_seconds"],expected)
                self.assertGreaterEqual(plan["metrics"]["min_f0_hz"],80)
                self.assertLessEqual(plan["metrics"]["max_f0_hz"],180)
                self.assertLessEqual(
                    plan["metrics"]["max_abs_micro_jitter_semitones"],
                    MAX_MICRO_JITTER_SEMITONES,
                )
                self.assertEqual(
                    plan["metrics"]["semantic_token_count"],len(parsed["tokens"])
                )

    def test_frames_sum_to_exact_reported_duration(self):
        plan=plan_text("Rocky calculate. 64. Good.",self.runtime,multiplier=2)
        total=sum(frame["duration_ms"] for frame in plan["frames"])/1000
        self.assertAlmostEqual(total,plan["metrics"]["total_duration_seconds"],places=6)

    def test_token_boundaries_remain_voiced_amplitude_dips_not_beep_gaps(self):
        plan=plan_text("Rocky calculate. 64. Good.",self.runtime,multiplier=2)
        boundaries=[
            frame for frame in plan["frames"] if frame["segment"]=="token_boundary"
        ]
        anchors=[
            frame for frame in plan["frames"] if frame["segment"].startswith("anchor_")
        ]
        self.assertTrue(boundaries)
        self.assertTrue(all(frame["voiced"] for frame in boundaries))
        self.assertTrue(all(frame["f0_hz"]>0 for frame in boundaries))
        self.assertGreater(min(frame["amplitude"] for frame in boundaries),0)
        self.assertLess(
            sum(frame["amplitude"] for frame in boundaries)/len(boundaries),
            sum(frame["amplitude"] for frame in anchors)/len(anchors),
        )

    def test_carrier_plan_is_deterministic(self):
        first=plan_text("Amaze amaze amaze!",self.runtime,multiplier=2)
        second=plan_text("Amaze amaze amaze!",self.runtime,multiplier=2)
        self.assertEqual(first,second)

    def test_profile_only_offers_renderer_hints_not_naturalness_claim(self):
        plan=plan_text("Rocky calculate. 64. Good.",self.runtime,multiplier=2)
        carrier=plan["carrier"]
        self.assertEqual(
            carrier["naturalness_status"],"NOT_RUN_REQUIRES_HUMAN_LISTENING"
        )
        self.assertEqual(len(carrier["formant_hint_hz"]),3)
        self.assertLess(carrier["subharmonic_mix_hint"],0.25)
        self.assertLess(carrier["breathiness_hint"],0.1)

    def test_unknown_lexical_fallback_is_not_hidden_by_acoustic_experiment(self):
        with self.assertRaisesRegex(ValueError,"fully semantic"):
            plan_text("Rocky calibrate spectrometer",self.runtime,multiplier=2)

    def test_benchmark_subjective_acceptance_stays_not_run(self):
        self.assertEqual(
            self.benchmark["subjective_acceptance"]["status"],
            "NOT_RUN_REQUIRES_HUMAN_LISTENING",
        )


if __name__=="__main__":
    unittest.main()
