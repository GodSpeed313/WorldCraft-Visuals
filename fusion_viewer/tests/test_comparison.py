"""Parent-to-fusion comparison (AUTH-016): data, page, and the rules it must not break.

Expected values are read from the golden cards on disk, an independent source from the
view builder, so a wrong label or dropped row in the builder or the page is caught."""

import json
import re
import unittest

from fusion_synthesis.loader import load_library

from fusion_viewer.build import TEMPLATE_PATH, render_html
from fusion_viewer.viewmodel import build_comparison, build_view, pair_key

from . import GOLDEN_DIR, run_harness

RAW_ID = re.compile(r"\b[a-z_]+\.[a-z_]+\b")


def golden_cards(view):
    """Golden cards on disk, keyed by the viewer's unordered pair key (file names keep the authored order)."""
    slug_of = {c["name"]: c["slug"] for c in view["characters"]}
    cards = {}
    for path in sorted(GOLDEN_DIR.glob("*.json")):
        card = json.loads(path.read_text(encoding="utf-8"))
        cards[pair_key(slug_of[card["sources"]["A"]], slug_of[card["sources"]["B"]])] = card
    return cards


class ComparisonDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view = build_view()
        cls.golden = golden_cards(cls.view)
        cls.library = load_library()

    def pairs(self):
        for key, rec in self.view["pairs"].items():
            yield key, rec["comparison"], self.golden[key]

    def test_every_authored_pair_has_a_comparison_and_there_are_five(self):
        self.assertEqual(len(list(self.pairs())), 5)

    def test_every_trait_outcome_is_carried_over_exactly(self):
        for key, cmp, card in self.pairs():
            with self.subTest(pair=key):
                self.assertEqual(len(cmp["traits"]), len(card["traits"]))
                want = {t["property_id"]: t for t in card["traits"]}
                for row in cmp["traits"]:
                    src = want[row["property_id"]]
                    self.assertEqual(row["outcome"], src["outcome"])
                    self.assertEqual(row["result_text"], src["result_text"])
                    self.assertEqual(row["reason"], src.get("reason"))
                    self.assertEqual(row["parent"], src["character"])

    def test_traits_are_in_the_parents_columns_a_then_b(self):
        for key, cmp, card in self.pairs():
            sides = [r["side"] for r in cmp["traits"]]
            self.assertEqual(sides, sorted(sides), key)
            self.assertEqual({r["parent"] for r in cmp["traits"]}, set(card["sources"].values()))

    def test_every_slot_is_present_with_authored_origin_and_delta(self):
        for key, cmp, card in self.pairs():
            with self.subTest(pair=key):
                self.assertEqual([s["slot"] for s in cmp["slots"]], list(card["appearance"]["slots"]))
                prov = {r["slot"]: r for r in card["visual_provenance"]}
                for s in cmp["slots"]:
                    self.assertEqual(s["origin"], prov[s["slot"]]["origin"])
                    self.assertEqual(s["fused"], card["appearance"]["slots"][s["slot"]])
                    self.assertEqual(s["design_delta"], prov[s["slot"]].get("design_delta"))
                    self.assertEqual([d["id"] for d in s["derived_from"]], prov[s["slot"]]["parent_ids"])

    def test_a_new_slot_is_never_given_a_parent_slot(self):
        for key, cmp, card in self.pairs():
            for s in cmp["slots"]:
                if s["origin"] == "new":
                    self.assertEqual([d["id"] for d in s["derived_from"]], [card["emergent_ability"]["id"]], (key, s["slot"]))
                    self.assertIsNone(s["design_delta"])

    def test_parent_descriptors_come_from_the_character_files(self):
        for key, cmp, card in self.pairs():
            chars = {side: self.library.characters[name] for side, name in card["sources"].items()}
            for s in cmp["slots"]:
                for side, field in (("A", "a"), ("B", "b")):
                    expected = [v.descriptor for v in chars[side].visual_traits if v.slot == s["slot"]]
                    self.assertEqual([s[field]] if s[field] is not None else [], expected)

    def test_labels_are_human_readable_names_and_not_raw_ids(self):
        for key, cmp, card in self.pairs():
            with self.subTest(pair=key):
                labelled = (
                    [r["label"] for r in cmp["traits"]]
                    + [d["label"] for r in cmp["slots"] for d in r["derived_from"]]
                    + [d["label"] for d in cmp["ability"]["derived_from"]]
                    + [a["label"] for a in cmp["ancestry"]]
                )
                self.assertTrue(labelled)
                for text in labelled:
                    self.assertIsNone(RAW_ID.search(text), text)
                    self.assertIn("(", text)  # "Name (Character)" or "(fused ability)"

    def test_a_trait_label_is_the_authored_name_plus_the_character(self):
        for key, cmp, card in self.pairs():
            for src, row in zip(sorted(card["traits"], key=lambda t: t["source"]), cmp["traits"]):
                self.assertEqual(row["label"], f"{src['name']} ({src['character']})")

    def test_ancestry_matches_the_card_and_keeps_the_raw_id(self):
        for key, cmp, card in self.pairs():
            self.assertEqual([a["id"] for a in cmp["ancestry"]], [a["id"] for a in card["ancestry"]])
            self.assertEqual([a["provenance"] for a in cmp["ancestry"]], [a["provenance"] for a in card["ancestry"]])
            self.assertEqual([d["id"] for d in cmp["ability"]["derived_from"]], card["emergent_ability"]["direct_ancestor_ids"])

    def test_unknown_ids_keep_the_raw_id_and_no_name_is_invented(self):
        key, rec = next(iter(self.view["pairs"].items()))
        card = json.loads(json.dumps(rec["card"]))
        card["ancestry"].append({"id": "zzz.unknown_thing", "kind": "source property", "character": "X", "provenance": "SOURCE_DERIVED"})
        names = list(card["sources"].values())
        cmp = build_comparison(card, self.library.characters[names[0]], self.library.characters[names[1]])
        self.assertEqual(cmp["ancestry"][-1]["label"], "zzz.unknown_thing")

    def test_the_tally_is_marked_computed_and_matches_the_labels(self):
        for key, cmp, card in self.pairs():
            self.assertTrue(cmp["tally"]["computed"])
            self.assertEqual(sum(cmp["tally"]["counts"].values()), len(card["traits"]))
            for outcome, n in cmp["tally"]["counts"].items():
                self.assertEqual(n, sum(1 for t in card["traits"] if t["outcome"] == outcome))

    def test_the_comparison_adds_no_claim_of_emergence_or_validation(self):
        text = json.dumps([rec["comparison"] for rec in self.view["pairs"].values()]).lower()
        for word in ("proves", "validated", "demonstrated emergence", "genuine emergence"):
            self.assertNotIn(word, text)


class ComparisonPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view = build_view()
        cls.snap = run_harness(render_html(cls.view))
        cls.golden = golden_cards(cls.view)

    def test_authored_pairs_show_the_comparison_and_unauthored_pairs_do_not(self):
        shown = hidden = 0
        for page in self.snap["pairs"]:
            if page["fusionName"]:
                shown += 1
                self.assertTrue(page["comparisonPresent"], (page["x"], page["y"]))
            else:
                hidden += 1
                self.assertFalse(page["comparisonPresent"])
                self.assertEqual(page["comparisonTraits"], [])
        self.assertEqual((shown, hidden), (10, 20))

    def test_every_trait_row_is_rendered_once_with_its_outcome_label_and_reason(self):
        for page in self.snap["pairs"]:
            if not page["fusionName"]:
                continue
            key = self.view["lookup"][page["x"]][page["y"]]
            card = self.golden[key]
            with self.subTest(pair=key):
                self.assertEqual(sorted(r["id"] for r in page["comparisonTraits"]), sorted(t["property_id"] for t in card["traits"]))
                rows = {r["id"]: r for r in page["comparisonTraits"]}
                for t in card["traits"]:
                    row = rows[t["property_id"]]
                    self.assertEqual(row["outcome"], t["outcome"])
                    self.assertIn(f"{t['name']} ({t['character']})", row["text"])
                    self.assertIn(t["result_text"], row["text"])
                    if t.get("reason"):
                        self.assertIn(t["reason"], row["text"])

    def test_every_slot_row_shows_both_parents_the_fusion_and_the_authored_change(self):
        for page in self.snap["pairs"]:
            if not page["fusionName"]:
                continue
            key = self.view["lookup"][page["x"]][page["y"]]
            cmp = self.view["pairs"][key]["comparison"]
            with self.subTest(pair=key):
                self.assertEqual([r["slot"] for r in page["comparisonSlots"]], [s["slot"] for s in cmp["slots"]])
                for row, s in zip(page["comparisonSlots"], cmp["slots"]):
                    self.assertEqual(row["origin"], s["origin"])
                    for part in (s["a"], s["b"], s["fused"]):
                        if part:
                            self.assertIn(part, row["text"])
                    if s["design_delta"]:
                        self.assertIn(s["design_delta"]["from"], row["text"])
                        self.assertIn(s["design_delta"]["to"], row["text"])

    def test_names_come_first_and_raw_ids_are_only_secondary(self):
        for page in self.snap["pairs"]:
            if not page["fusionName"]:
                continue
            for row in page["comparisonTraits"]:
                self.assertRegex(row["text"], r"\(.+\)")
                self.assertIn("id: " + row["id"], row["text"])
            key = self.view["lookup"][page["x"]][page["y"]]
            text = page["comparisonText"]
            cmp = self.view["pairs"][key]["comparison"]
            ids = [r["property_id"] for r in cmp["traits"]] + [a["id"] for a in cmp["ancestry"]]
            for ident in ids:
                self.assertIn("id: " + ident, text)  # every raw id is present, as a labelled secondary line
                self.assertNotIn(ident + " ", text.replace("id: " + ident, ""))  # and never on its own

    def test_the_page_says_the_labels_are_the_authors_and_the_tally_is_computed(self):
        for page in self.snap["pairs"]:
            if page["fusionName"]:
                self.assertIn("are the authors' own", page["comparisonText"])
                self.assertIn("does not measure", page["comparisonText"])
                self.assertIn("(computed here)", page["comparisonTally"])


class ComparisonTemplateTests(unittest.TestCase):
    def test_phone_layout_rules_exist_for_the_comparison(self):
        template = TEMPLATE_PATH.read_bytes().decode("utf-8")
        self.assertRegex(template, r"@media \(max-width: 700px\)[^}]*\.cmp-head \{ display: none; \}")
        self.assertIn(".cmp-row { grid-template-columns: minmax(0, 1fr); }", template)
        self.assertIn(".cmp-cell .cell-label { display: block; }", template)


if __name__ == "__main__":
    unittest.main()
