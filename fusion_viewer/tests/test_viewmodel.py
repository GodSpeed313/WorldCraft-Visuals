"""View data: pair resolution, authored cards, and the status block (Path A)."""

import json
import unittest
from itertools import combinations

from fusion_synthesis.loader import golden_paths, load_library

from fusion_viewer.viewmodel import NOT_SYNTHESIZED, NOTICE, build_view, pair_key, resolve


class ViewModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()
        cls.view = build_view()
        cls.names = [c["name"] for c in cls.view["characters"]]

    def authored_keys(self):
        slug_of = {c.name: c.slug for c in self.library.characters.values()}
        return {pair_key(slug_of[p.a], slug_of[p.b]) for p in self.library.pairs}

    def test_the_viewer_lists_every_character_of_the_library(self):
        self.assertEqual(self.names, list(self.library.characters))

    def test_all_fifteen_unordered_combinations_resolve_in_either_order(self):
        combos = list(combinations(self.names, 2))
        self.assertEqual(len(combos), 15)
        authored = self.authored_keys()
        slug_of = {c["name"]: c["slug"] for c in self.view["characters"]}
        for first, second in combos:
            forward, backward = resolve(self.view, first, second), resolve(self.view, second, first)
            with self.subTest(pair=f"{first} x {second}"):
                self.assertEqual(forward, backward)
                if pair_key(slug_of[first], slug_of[second]) in authored:
                    self.assertIsNotNone(forward)
                else:
                    self.assertIsNone(forward)

    def test_current_corpus_has_five_authored_and_ten_unauthored_pairs(self):
        # Acceptance baseline for the corpus at the time of authorization. Update it only
        # when authored pairs are added through their own authorization.
        results = [resolve(self.view, a, b) for a, b in combinations(self.names, 2)]
        self.assertEqual(sum(r is not None for r in results), 5)
        self.assertEqual(sum(r is None for r in results), 10)

    def test_combinations_list_marks_exactly_the_authored_pairs(self):
        self.assertEqual(len(self.view["combinations"]), 15)
        marked = {pair_key(c["a"], c["b"]) for c in self.view["combinations"] if c["pair"]}
        self.assertEqual(marked, self.authored_keys())

    def test_lookup_is_symmetric_and_excludes_self_pairs(self):
        for a, row in self.view["lookup"].items():
            self.assertNotIn(a, row)
            for b, key in row.items():
                self.assertEqual(key, self.view["lookup"][b][a])

    def test_unknown_or_identical_characters_resolve_to_nothing(self):
        self.assertIsNone(resolve(self.view, self.names[0], self.names[0]))
        self.assertIsNone(resolve(self.view, self.names[0], "not a character"))

    def test_every_authored_card_equals_the_golden_json(self):
        for pair in self.library.pairs:
            _txt, json_path = golden_paths(self.library.data_dir, pair)
            golden = json.loads(json_path.read_bytes().decode("utf-8"))
            with self.subTest(pair=pair.slug):
                self.assertEqual(resolve(self.view, pair.a, pair.b)["card"], golden)
                self.assertEqual(resolve(self.view, pair.b, pair.a)["card"], golden)

    def test_the_default_selection_is_an_authored_pair(self):
        a, b = self.view["default_selection"]
        self.assertIsNotNone(self.view["lookup"][a][b])

    def test_the_missing_result_text_is_the_required_sentence(self):
        self.assertEqual(NOT_SYNTHESIZED, "Not yet synthesized — no authored result exists for this pair.")
        self.assertEqual(self.view["not_synthesized"], NOT_SYNTHESIZED)
        self.assertIn("does not claim demonstrated emergence", NOTICE)


class StatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view = build_view()

    def test_no_authored_card_is_labelled_independently_validated(self):
        for key, pair in self.view["pairs"].items():
            status = pair["status"]
            with self.subTest(pair=key):
                self.assertFalse(status["independent_validation"]["recorded"])
                self.assertIn("Not independently validated", status["summary"])
                self.assertNotIn("Independently validated", status["summary"])
                self.assertFalse(status["experimental"]["recorded"])

    def test_the_data_really_has_no_validation_or_experimental_field(self):
        # The status block says "not recorded" because the data has nothing to record. If an
        # authored card ever gains such a field, this fails so the viewer is updated on purpose.
        library = load_library()
        for pair in self.view["pairs"].values():
            blob = json.dumps(pair["card"]).lower()
            for word in ("independent_validation", "validated", "experimental"):
                self.assertNotIn(word, blob)
        for path in sorted((library.data_dir / "pairs").glob("*.json")):
            text = path.read_text(encoding="utf-8").lower()
            for word in ("validated", "experimental"):
                self.assertNotIn(word, text, f"{path.name} now mentions {word!r}; update the viewer's status logic")

    def test_invented_bridge_is_visible_in_the_summary_and_details(self):
        seen = 0
        for pair in self.view["pairs"].values():
            card, status = pair["card"], pair["status"]
            invented = "INVENTED_BRIDGE" in (
                card["emergent_ability"]["provenance"],
                card["emergent_ability"]["governing_rule"]["provenance"],
            )
            with self.subTest(pair=pair["key"]):
                self.assertEqual(status["emergent_provenance"]["bridge_invented"], invented)
                self.assertEqual("Bridge invented" in status["summary"], invented)
                seen += invented
        self.assertGreater(seen, 0, "the corpus has no INVENTED_BRIDGE card to exercise this check")

    def test_zero_evaluated_conditions_is_disclosed_and_not_in_the_headline(self):
        for pair in self.view["pairs"].values():
            status = pair["status"]
            with self.subTest(pair=pair["key"]):
                self.assertEqual(
                    status["mechanical_checks"]["evaluated_conditions"], pair["card"]["compatibility"]["evaluated_conditions"]
                )
                headline = " ".join(status["summary"])
                self.assertNotIn("evaluated", headline)
                self.assertNotIn("COMPATIBLE", headline)
                self.assertIn("not proof of genuine emergence", status["mechanical_checks"]["caveat"])

    def test_the_summary_has_three_short_parts(self):
        for pair in self.view["pairs"].values():
            self.assertEqual(len(pair["status"]["summary"]), 3)
            self.assertEqual(pair["status"]["summary"][0], "Authored")

    def test_leak_check_limits_are_carried_from_the_card(self):
        for pair in self.view["pairs"].values():
            leak = pair["status"]["leak_check"]
            self.assertEqual(leak["claim"], pair["card"]["leak_check"]["claim"])
            self.assertIn("implemented detector only", leak["claim"])


if __name__ == "__main__":
    unittest.main()
