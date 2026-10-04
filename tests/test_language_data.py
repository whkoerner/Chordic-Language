import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGUAGE = ROOT / "language"
FILES = {
    "dictionary": LANGUAGE / "dictionary.json",
    "grammar": LANGUAGE / "grammar.json",
    "phonology": LANGUAGE / "phonology.json",
    "gestures": LANGUAGE / "gestures.json",
    "examples": LANGUAGE / "examples.json",
}
ALLOWED_ENTRY_STATUSES = {
    "experimental",
    "candidate",
    "stable",
    "deprecated",
    "reserved",
}


def load(name):
    with FILES[name].open("r", encoding="utf-8") as handle:
        return json.load(handle)


class LanguageDataTests(unittest.TestCase):
    def test_all_language_json_files_parse(self):
        for name in FILES:
            with self.subTest(name=name):
                self.assertIsInstance(load(name), dict)

    def test_all_language_files_report_v0_0(self):
        for name in FILES:
            with self.subTest(name=name):
                self.assertEqual(load(name).get("language_version"), "0.0")

    def test_dictionary_ids_are_unique(self):
        entries = load("dictionary")["entries"]
        ids = [entry["id"] for entry in entries]
        self.assertEqual(len(ids), len(set(ids)))

    def test_grammar_rule_ids_are_unique(self):
        rules = load("grammar")["rules"]
        ids = [rule["id"] for rule in rules]
        self.assertEqual(len(ids), len(set(ids)))

    def test_gesture_ids_are_unique(self):
        gestures = load("gestures")["gestures"]
        ids = [gesture["id"] for gesture in gestures]
        self.assertEqual(len(ids), len(set(ids)))

    def test_seed_example_ids_are_unique(self):
        examples = load("examples")["examples"]
        ids = [example["id"] for example in examples]
        self.assertEqual(len(ids), len(set(ids)))

    def test_unsupported_examples_have_no_invented_translation(self):
        for example in load("examples")["examples"]:
            if example["support_status"] == "unsupported":
                with self.subTest(id=example["id"]):
                    self.assertIsNone(example["semantic_representation"])
                    self.assertIsNone(example["chordic_form"])

    def test_canonical_tonal_forms_do_not_collide(self):
        forms = []
        for entry in load("dictionary")["entries"]:
            form = entry.get("tonal_representation")
            if form is not None and entry.get("status") != "deprecated":
                forms.append(form)
        serialized = [json.dumps(form, sort_keys=True) for form in forms]
        self.assertEqual(len(serialized), len(set(serialized)))

    def test_reserved_patterns_are_not_used_by_dictionary(self):
        reserved = {
            json.dumps(pattern, sort_keys=True)
            for pattern in load("phonology")["reserved_patterns"]
        }
        for entry in load("dictionary")["entries"]:
            form = entry.get("tonal_representation")
            if form is not None:
                self.assertNotIn(json.dumps(form, sort_keys=True), reserved)

    def test_non_null_seed_gesture_references_exist(self):
        gesture_ids = {g["id"] for g in load("gestures")["gestures"]}
        for example in load("examples")["examples"]:
            requirement = example.get("gesture_requirement")
            if not requirement:
                continue
            gesture_id = requirement.get("canonical_gesture_id")
            if gesture_id is not None:
                self.assertIn(gesture_id, gesture_ids)

    def test_dictionary_entry_statuses_are_known(self):
        for entry in load("dictionary")["entries"]:
            with self.subTest(id=entry.get("id")):
                self.assertIn(entry["status"], ALLOWED_ENTRY_STATUSES)


if __name__ == "__main__":
    unittest.main()
