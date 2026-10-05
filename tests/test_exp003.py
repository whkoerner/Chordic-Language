import unittest
from tools.exp003_benchmark import analyze, load, parse_text, RUNTIME, CORPUS

class Exp003Tests(unittest.TestCase):
    def setUp(self):
        self.runtime=load(RUNTIME)
        self.corpus=load(CORPUS)
        self.candidate=self.runtime["candidate"]

    def test_benchmark_reproduces_stored_coverage_and_timing(self):
        self.assertEqual(analyze(),self.corpus["results"])

    def test_open_conversation_is_coverage_first(self):
        rows=[row for row in analyze() if row["class"]!="seed"]
        self.assertEqual(len(rows),11)
        self.assertTrue(all(row["semantic_coverage_percent"]==100.0 for row in rows))
        self.assertTrue(all(row["fallback_span_count"]==0 for row in rows))
        self.assertTrue(all(row["total_duration_seconds"]<=10 for row in rows))

    def test_math_is_compositional_not_sentence_id(self):
        parsed=parse_text("8 times 8 is 64",self.runtime)
        self.assertEqual(parsed["tokens"],["NUM.8","OP.MUL","NUM.8","NUM.6","NUM.4"])
        self.assertEqual(parsed["fallback_spans"],[])
        surfaces={row["text"].lower() for row in self.runtime["surface_forms"]}
        self.assertNotIn("8 times 8 is 64",surfaces)

    def test_unseen_words_are_explicit_fallback(self):
        parsed=parse_text("Rocky calibrate spectrometer",self.runtime)
        self.assertEqual(parsed["tokens"],["ENTITY.ROCKY"])
        self.assertEqual(parsed["fallback_spans"],["calibrate","spectrometer"])
        self.assertGreater(parsed["fallback_bytes"],0)
        self.assertLess(parsed["semantic_coverage_percent"],100)

    def test_contour_registry_has_symbolic_distance(self):
        codes=[tuple(row["contour_code"]) for row in self.candidate["tokens"]]
        self.assertEqual(len(codes),len(set(codes)))
        def hamming(a,b): return sum(x!=y for x,y in zip(a,b))
        minimum=min(hamming(a,b) for i,a in enumerate(codes) for b in codes[i+1:])
        self.assertGreaterEqual(minimum,2)

    def test_relative_pitch_range_is_human_scale_not_absolute_note_identity(self):
        acoustics=self.candidate["acoustics"]
        offsets=list(acoustics["pitch_offsets_semitones"].values())
        self.assertEqual(max(offsets)-min(offsets),8)
        for baseline in acoustics["baseline_hz_examples"]:
            low=baseline*2**(min(offsets)/12); high=baseline*2**(max(offsets)/12)
            self.assertGreaterEqual(low,80)
            self.assertLessEqual(high,350)

if __name__=="__main__":
    unittest.main()
