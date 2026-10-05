import unittest
from tools.exp003_v2_benchmark import analyze, load, parse_text, RUNTIME, CORPUS

class Exp003V2Tests(unittest.TestCase):
    def setUp(self):
        self.runtime=load(RUNTIME)
        self.corpus=load(CORPUS)
        self.candidate=self.runtime["candidate"]

    def test_real_windows_replies_become_full_semantic_coverage(self):
        computed={row["id"]:row for row in analyze()}
        for source in self.corpus["results"]:
            expected=source["v2_model"]
            actual=computed[source["id"]]
            self.assertEqual(actual["semantic_tokens"], expected["semantic_tokens"])
            self.assertEqual(actual["semantic_coverage_percent"], 100.0)
            self.assertEqual(actual["fallback_span_count"], 0)
            self.assertEqual(actual["fallback_bytes"], 0)
            self.assertAlmostEqual(actual["total_duration_seconds"], expected["total_duration_seconds"], places=3)
            self.assertLessEqual(actual["total_duration_seconds"], 10.0)

    def test_spoken_numbers_are_compositional(self):
        parsed=parse_text("Eight times eight. Sixty four.", self.runtime)
        self.assertEqual(parsed["tokens"], ["NUM.8","OP.MUL","NUM.8","NUM.6","NUM.4"])
        self.assertEqual(parsed["fallback_spans"], [])
        surfaces={row["text"].lower() for row in self.runtime["surface_forms"]}
        self.assertNotIn("sixty four", surfaces)

    def test_problem_solve_is_primitive_composition(self):
        parsed=parse_text("Rocky problem solve.", self.runtime)
        self.assertEqual(parsed["tokens"], ["ENTITY.ROCKY","ENTITY.PROBLEM","ACTION.SOLVE"])
        self.assertEqual(parsed["fallback_spans"], [])

    def test_low_register_reference_and_fallback_band(self):
        acoustics=self.candidate["acoustics"]
        self.assertEqual(acoustics["reference_baseline_hz"],120)
        self.assertLessEqual(acoustics["recommended_output_band_hz"][1],180)
        self.assertEqual(acoustics["fallback_reference_hz"],105)
        offsets=list(acoustics["pitch_offsets_semitones"].values())
        semantic=[120*2**(offset/12) for offset in offsets]
        fallback=[105*2**(offset/12) for offset in offsets]
        self.assertLess(max(semantic), 155)
        self.assertLess(max(fallback), 135)

    def test_code_family_still_collision_free(self):
        codes=[tuple(row["contour_code"]) for row in self.candidate["tokens"]]
        self.assertEqual(len(codes),108)
        self.assertEqual(len(codes),len(set(codes)))
        minimum=min(sum(a!=b for a,b in zip(left,right)) for i,left in enumerate(codes) for right in codes[i+1:])
        self.assertGreaterEqual(minimum,2)

    def test_unknown_words_still_fallback(self):
        parsed=parse_text("Rocky calibrate spectrometer",self.runtime)
        self.assertEqual(parsed["tokens"],["ENTITY.ROCKY"])
        self.assertEqual(parsed["fallback_spans"],["calibrate","spectrometer"])

if __name__=="__main__":
    unittest.main()
