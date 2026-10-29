"""Registry binding (AUTH-011 §6 test 7).

AUTHORIZED EXCEPTION. This file, and only this file, may read the legacy
modality module as TEXT and parse it with Python's `ast` module, solely to
extract CHARACTER_REGISTRY's keys and modality values with `ast.literal_eval`,
for read-only structural validation. It must not import, execute, compile or
load that module, and must not open it for writing. test_boundaries enforces
all of that. If the registry ever stops being a pure literal, the test below
FAILS with a clear message; it never skips.
"""

import ast
import unittest
from pathlib import Path

from fusion_synthesis.loader import load_library
from fusion_synthesis.schema import match_tokens

from . import REPO_ROOT

REGISTRY_SOURCE = REPO_ROOT / "modality_classifier.py"
REGISTRY_NAME = "CHARACTER_" + "REGISTRY"


def read_registry() -> dict:
    tree = ast.parse(REGISTRY_SOURCE.read_text(encoding="utf-8"), filename=str(REGISTRY_SOURCE))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == REGISTRY_NAME for t in node.targets):
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, SyntaxError) as exc:
                raise AssertionError(
                    f"{REGISTRY_NAME} is no longer a pure literal ({exc}); this binding test reads it "
                    "structurally and will not import or execute the legacy module"
                ) from None
            if not isinstance(value, dict):
                raise AssertionError(f"{REGISTRY_NAME} is not a dict literal")
            return value
    raise AssertionError(f"{REGISTRY_NAME} was not found at module level in {REGISTRY_SOURCE.name}")


class RegistryBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = read_registry()
        cls.library = load_library()

    def test_the_registry_is_read_structurally(self):
        self.assertGreater(len(self.registry), 0)
        for name, row in self.registry.items():
            self.assertIn("modality", row, name)

    def test_every_card_name_is_a_registry_key(self):
        for name in self.library.characters:
            with self.subTest(character=name):
                self.assertIn(name, self.registry, f"{name!r} has a card but is not in the registry")

    def test_every_pair_references_registered_characters(self):
        for pair in self.library.pairs:
            with self.subTest(pair=pair.slug):
                self.assertIn(pair.a, self.registry)
                self.assertIn(pair.b, self.registry)

    def test_real_people_are_out_of_scope(self):
        """LEGACY modality marks real historical figures; Phase 1 is fictional characters only."""
        for name in self.library.characters:
            with self.subTest(character=name):
                self.assertNotEqual(self.registry[name]["modality"], "LEGACY")

    def test_no_style_allowlist_term_shares_a_token_with_a_registry_key(self):
        for term in self.library.allowlist.terms:
            term_tokens = set(match_tokens(term))
            for key in self.registry:
                with self.subTest(term=term, key=key):
                    self.assertFalse(term_tokens & set(match_tokens(key)))

    def test_cards_bind_by_name_only_and_carry_no_registry_data(self):
        """Independent cards (AD-1): nothing in a card is read from, or copied out of, the registry."""
        for card in self.library.characters.values():
            for prop in card.properties:
                self.assertNotIn(prop.name, [row.get("trait") for row in self.registry.values()])


if __name__ == "__main__":
    unittest.main()
