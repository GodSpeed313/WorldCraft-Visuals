"""The generated page, run under node with a fake DOM (see harness.js)."""

import re
import unittest
from itertools import combinations

from fusion_viewer.build import TEMPLATE_PATH, render_html
from fusion_viewer.viewmodel import NOT_SYNTHESIZED, NOTICE, build_view

from . import run_harness

HEADLINE_FORBIDDEN = ("evaluated", "COMPATIBLE", "validated by")


class PageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view = build_view()
        cls.html = render_html(cls.view)
        cls.snap = run_harness(cls.html)
        cls.by_selection = {(p["x"], p["y"]): p for p in cls.snap["pairs"]}

    def test_the_page_script_ran_and_made_no_forbidden_calls(self):
        # run_harness raises if the script used fetch/XHR/innerHTML/document.write, none of which exist in it.
        self.assertTrue(self.snap["pairs"])

    def test_every_ordered_selection_of_two_distinct_characters_was_exercised(self):
        n = len(self.view["characters"])
        self.assertEqual(len(self.snap["pairs"]), n * (n - 1))

    def test_all_fifteen_pairs_show_the_right_result_in_either_order(self):
        slugs = [c["slug"] for c in self.view["characters"]]
        self.assertEqual(len(list(combinations(slugs, 2))), 15)
        for first, second in combinations(slugs, 2):
            key = self.view["lookup"][first][second]
            for x, y in ((first, second), (second, first)):
                page = self.by_selection[(x, y)]
                with self.subTest(selection=f"{x} then {y}"):
                    self.assertEqual(sorted(page["selected"]), sorted([x, y]))
                    self.assertEqual(sorted(page["sourceNames"]), sorted([x, y]))
                    if key:
                        self.assertEqual(page["fusionName"], self.view["pairs"][key]["card"]["fusion_name"])
                        self.assertIsNone(page["missingText"])
                    else:
                        self.assertEqual(page["missingText"], NOT_SYNTHESIZED)
                        self.assertIsNone(page["fusionName"])
                        self.assertIsNone(page["statusLine"])

    def test_unauthored_pairs_offer_no_action_and_generate_nothing(self):
        missing = [p for p in self.snap["pairs"] if p["missingText"]]
        self.assertTrue(missing)
        for page in missing:
            with self.subTest(selection=(page["x"], page["y"])):
                self.assertEqual(page["interactiveInResult"], [])
                self.assertNotIn("generate", page["resultText"].lower())

    def test_the_page_opens_on_an_authored_pair(self):
        initial = self.snap["initial"]
        self.assertEqual(initial["selected"], self.view["default_selection"])
        self.assertIsNotNone(initial["fusionName"])
        self.assertIsNone(initial["missingText"])

    def test_the_status_line_matches_the_data_and_the_details_start_collapsed(self):
        for page in self.snap["pairs"]:
            if not page["fusionName"]:
                continue
            key = self.view["lookup"][page["x"]][page["y"]]
            expected = " · ".join(self.view["pairs"][key]["status"]["summary"])
            with self.subTest(pair=key):
                self.assertEqual(page["statusLine"], expected)
                self.assertNotIn("Independently validated", page["statusLine"])
                for word in HEADLINE_FORBIDDEN:
                    self.assertNotIn(word, page["statusLine"])
                self.assertTrue(page["detailsPresent"])
                self.assertFalse(page["detailsOpenAttr"], "status details must start collapsed")

    def test_expanded_details_cover_every_required_topic_and_disclose_zero_conditions(self):
        required = (
            "Authored provenance",
            "Mechanical checks",
            "Independent validation",
            "Experimental status",
            "Emergent-ability provenance",
            "Leak check",
            "0 activation conditions evaluated",
            "not proof of genuine emergence",
            "No independent validation record exists",
            "Not recorded (unknown)",
        )
        authored = [p for p in self.snap["pairs"] if p["fusionName"]]
        self.assertTrue(authored)
        for page in authored:
            with self.subTest(pair=(page["x"], page["y"])):
                for text in required:
                    self.assertIn(text, page["detailsText"])

    def test_invented_bridge_is_visible_on_the_page(self):
        flagged = 0
        for page in self.snap["pairs"]:
            if not page["fusionName"]:
                continue
            key = self.view["lookup"][page["x"]][page["y"]]
            if self.view["pairs"][key]["status"]["emergent_provenance"]["bridge_invented"]:
                flagged += 1
                self.assertIn("Bridge invented", page["statusLine"])
                self.assertIn("INVENTED_BRIDGE", page["detailsText"])
                self.assertIn("INVENTED_BRIDGE", page["resultText"])
        self.assertGreater(flagged, 0)

    def test_the_authored_only_notice_is_always_visible(self):
        self.assertEqual(self.snap["initial"]["footerText"], NOTICE)
        for page in self.snap["pairs"]:
            self.assertEqual(page["footerText"], NOTICE)
            if page["fusionName"]:
                self.assertIn(NOTICE, page["resultText"])

    def test_selection_rules(self):
        slugs = [c["slug"] for c in self.view["characters"]]
        self.assertEqual(self.snap["afterDoubleClick"]["selected"], [])  # clicking again deselects; never two copies
        self.assertEqual(sorted(self.snap["afterThird"]["selected"]), sorted(slugs[1:3]))  # the oldest is replaced


class TemplateScanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = TEMPLATE_PATH.read_bytes().decode("utf-8")
        cls.script = re.search(r"<script>([\s\S]*?)</script>", cls.template).group(1)

    def test_no_network_api_or_markup_injection_sink_in_the_page_script(self):
        for name in (
            "fetch", "XMLHttpRequest", "WebSocket", "EventSource", "sendBeacon", "importScripts",
            "innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "eval(", "new Function", "localStorage",
        ):
            self.assertNotIn(name, self.script, name)
        self.assertIsNone(re.search(r"https?:", self.script))
        self.assertIsNone(re.search(r"\bimport\s*\(", self.script))

    def test_only_google_fonts_are_requested_and_a_content_security_policy_forbids_the_rest(self):
        urls = set(re.findall(r"https?://[^\s\"')]+", self.template))
        self.assertTrue(all(u.startswith(("https://fonts.googleapis.com", "https://fonts.gstatic.com")) for u in urls), urls)
        self.assertIn("Content-Security-Policy", self.template)
        self.assertIn("default-src 'none'", self.template)
        self.assertNotIn("connect-src", self.template)  # falls back to default-src 'none'
        self.assertNotIn("<script src", self.template.lower())

    def test_the_required_fonts_have_system_fallbacks(self):
        self.assertIn("Syne", self.template)
        self.assertIn("Space Mono", self.template)
        self.assertRegex(self.template, r"--sans:\s*'Syne',\s*system-ui")
        self.assertRegex(self.template, r"--mono:\s*'Space Mono',\s*ui-monospace")

    def test_the_page_has_no_live_synthesis_control(self):
        lowered = self.template.lower()
        for word in ("synthesize now", "generate fusion", "run synthesis", "call the model", "api key"):
            self.assertNotIn(word, lowered)

    def test_the_page_is_responsive(self):
        self.assertIn('name="viewport"', self.template)
        self.assertIn("@media (max-width", self.template)


if __name__ == "__main__":
    unittest.main()
