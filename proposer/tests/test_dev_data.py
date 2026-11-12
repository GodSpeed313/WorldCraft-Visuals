"""IMP-001 M1: the development library loads, and the production library is untouched."""

import unittest
from pathlib import Path

from fusion_synthesis.loader import load_library

REPO_ROOT = Path(__file__).resolve().parents[2]
DEV_DIR = REPO_ROOT / "dev_data" / "prop001"
PROD_DIR = REPO_ROOT / "fusion_synthesis" / "data"

DEV_NAMES = {"Ilse Marrow", "Sable Quillon", "Tamsin Vey", "Pell Dunmore"}
DEV_SLUGS = {"ilse_marrow", "sable_quillon", "tamsin_vey", "pell_dunmore"}
REGISTERED_NAMES = {"James Bond", "Kino", "Maka", "Re-l Mayer", "The Medicine Seller", "Vash"}


class DevelopmentLibraryTests(unittest.TestCase):
    def test_dev_data_loads_through_the_loader(self):
        library = load_library(data_dir=DEV_DIR)
        self.assertEqual(set(library.characters), DEV_NAMES)
        self.assertEqual(library.pairs, ())
        for card in library.characters.values():
            self.assertEqual(card.epistemic_status, "FICTIONAL")
            self.assertEqual(len(card.properties), 6)
            self.assertEqual(len(card.visual_traits), 7)

    def test_the_development_allowlist_is_an_exact_copy_of_the_production_one(self):
        self.assertEqual(
            (DEV_DIR / "style_allowlist.json").read_bytes(),
            (PROD_DIR / "style_allowlist.json").read_bytes(),
        )

    def test_the_development_pairs_folder_holds_no_pair_file(self):
        self.assertEqual(sorted(DEV_DIR.joinpath("pairs").glob("*.json")), [])


class ProductionLibraryTests(unittest.TestCase):
    def test_production_data_still_loads_with_only_the_registered_characters(self):
        library = load_library()
        self.assertEqual(set(library.characters), REGISTERED_NAMES)
        self.assertEqual(len(library.pairs), 5)
        self.assertFalse(set(library.characters) & DEV_NAMES)

    def test_no_production_data_file_mentions_a_development_character(self):
        for path in sorted(PROD_DIR.rglob("*")):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8").lower()
            with self.subTest(file=str(path.relative_to(REPO_ROOT))):
                for name in DEV_NAMES | DEV_SLUGS:
                    self.assertNotIn(name.lower(), text)


if __name__ == "__main__":
    unittest.main()
