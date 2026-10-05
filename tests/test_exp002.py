import unittest
from tools.exp002_benchmark import analyze, ct2_ms, load, CORPUS

class Exp002Tests(unittest.TestCase):
    def setUp(self):
        self.analysis=analyze()
        self.corpus=load(CORPUS)

    def test_rocky_ct2_baseline_snapshot_matches_documented_examples(self):
        baseline=self.corpus["rocky_ct2_baseline"]
        self.assertEqual(ct2_ms("hello robot",baseline),3165)
        self.assertEqual(ct2_ms("x"*384,baseline),31570)

    def test_normal_conversation_meets_target_at_unchanged_three_x_speed(self):
        metrics=self.analysis["metrics"]["normal"]
        self.assertEqual(metrics["candidate"]["percent_at_or_below_10_seconds"],100.0)
        self.assertEqual(metrics["candidate"]["count_over_10_seconds"],0)
        self.assertLessEqual(metrics["candidate"]["max_seconds"],10)
        self.assertLess(metrics["candidate"]["mean_seconds"],metrics["baseline"]["mean_seconds"])

    def test_common_expressions_are_shorter(self):
        metrics=self.analysis["metrics"]["common"]
        self.assertLess(metrics["candidate"]["mean_seconds"],4)
        self.assertLess(metrics["candidate"]["mean_seconds"],metrics["baseline"]["mean_seconds"])

    def test_symbolic_collision_and_ambiguity_checks(self):
        self.assertEqual(self.analysis["exact_collisions"],[])
        self.assertEqual(self.analysis["sequence_collisions"],[])
        self.assertEqual(self.analysis["framed_prefix_ambiguity_count"],0)
        self.assertGreater(len(self.analysis["near_collisions"]),0)
        self.assertTrue(all(distance>=2 for distance in self.analysis["critical_distances"].values()))

    def test_registered_intents_round_trip_to_same_canonical_english(self):
        self.assertTrue(all(row["round_trip_ok"] for row in self.analysis["rows"]))
        self.assertEqual(len(self.analysis["rows"]),37)

if __name__=="__main__":
    unittest.main()
