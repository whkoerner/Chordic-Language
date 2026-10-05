import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
V3=ROOT/"language"/"runtime"/"exp-003-runtime-export-v3.json"

class Exp003V3AcousticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runtime=json.loads(V3.read_text(encoding="utf-8"))
        cls.acoustics=cls.runtime["candidate"]["acoustics"]

    def test_v3_prefers_vocal_renderer_without_changing_semantic_code(self):
        self.assertEqual(self.runtime["export_id"],"EXP-003-runtime-v3")
        self.assertEqual(self.acoustics["recommended_renderer"],"vocal-v1")
        profile=self.acoustics["renderer_profiles"]["vocal-v1"]
        self.assertTrue(profile["phase_continuity"])
        self.assertLessEqual(profile["max_micro_pitch_jitter_semitones"],0.12)
        self.assertIn("low rumble",profile["intended_character"])

    def test_default_learning_conversation_speed_is_two(self):
        self.assertEqual(self.acoustics["default_duration_multiplier"],2)

    def test_pitch_band_stays_low(self):
        baseline=self.acoustics["reference_baseline_hz"]
        offsets=self.acoustics["pitch_offsets_semitones"].values()
        hz=[baseline*2**(offset/12) for offset in offsets]
        self.assertLess(max(hz),180)
        self.assertGreater(min(hz),80)

if __name__=="__main__":
    unittest.main()
