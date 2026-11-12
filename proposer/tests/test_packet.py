"""IMP-001 M1: the packet holds exactly the permitted inputs and is byte-reproducible."""

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from fusion_synthesis.loader import load_library
from proposer.packet import (
    CHARACTER_DIR,
    REQUIREMENTS_PATH,
    SCHEMA_PATH,
    PacketInputError,
    build_packet,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTERED_NAMES = ("James Bond", "Kino", "Maka", "Re-l Mayer", "The Medicine Seller", "Vash")
REGISTERED_SLUGS = ("james_bond", "kino", "maka", "re_l_mayer", "the_medicine_seller", "vash")


def real(rel: Path) -> Path:
    return REPO_ROOT / rel


def build_real(a="ilse_marrow", b="sable_quillon", **kw):
    return build_packet(
        real(CHARACTER_DIR / f"{a}.json"),
        real(CHARACTER_DIR / f"{b}.json"),
        real(REQUIREMENTS_PATH),
        real(SCHEMA_PATH),
        **kw,
    )


class TempRoot(unittest.TestCase):
    """A scratch copy of exactly the files a packet may use, so the real tree is never touched."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        shutil.copytree(REPO_ROOT / "dev_data" / "prop001", self.root / "dev_data" / "prop001")
        (self.root / REQUIREMENTS_PATH).parent.mkdir(parents=True)
        shutil.copy(real(REQUIREMENTS_PATH), self.root / REQUIREMENTS_PATH)
        (self.root / SCHEMA_PATH).parent.mkdir(parents=True)
        shutil.copy(real(SCHEMA_PATH), self.root / SCHEMA_PATH)

    def build(self, a="ilse_marrow", b="sable_quillon"):
        return build_packet(
            self.root / CHARACTER_DIR / f"{a}.json",
            self.root / CHARACTER_DIR / f"{b}.json",
            self.root / REQUIREMENTS_PATH,
            self.root / SCHEMA_PATH,
            repo_root=self.root,
        )


class PermittedInputsTests(TempRoot):
    def test_the_packet_contains_exactly_the_four_permitted_inputs(self):
        packet = build_real()
        self.assertEqual(sorted(packet.data), ["characters", "pair_schema_reference", "requirements", "schema"])
        self.assertEqual(
            [c["path"] for c in packet.data["characters"]],
            ["dev_data/prop001/characters/ilse_marrow.json", "dev_data/prop001/characters/sable_quillon.json"],
        )
        self.assertEqual(packet.data["requirements"]["path"], "proposer/inputs/req_001_v1.0_sections_1-5.md")
        self.assertEqual(packet.data["pair_schema_reference"]["path"], "fusion_synthesis/schema.py")

    def test_embedded_texts_are_the_files_themselves(self):
        packet = build_real()
        self.assertEqual(packet.data["characters"][0]["text"], real(CHARACTER_DIR / "ilse_marrow.json").read_text(encoding="utf-8"))
        self.assertEqual(packet.data["requirements"]["text"], real(REQUIREMENTS_PATH).read_text(encoding="utf-8"))

    def test_the_requirements_text_has_no_reviewer_appendix(self):
        self.assertNotIn("Reviewer appendix", build_real().data["requirements"]["text"])
        self.assertTrue(build_real().data["requirements"]["text"].startswith("## 1. "))

    def test_every_development_character_is_accepted(self):
        for name in ("ilse_marrow", "sable_quillon", "tamsin_vey", "pell_dunmore"):
            with self.subTest(name=name):
                other = "pell_dunmore" if name != "pell_dunmore" else "ilse_marrow"
                self.assertEqual(len(self.build(name, other).data["characters"]), 2)

    def test_a_production_character_is_rejected(self):
        with self.assertRaises(PacketInputError):
            build_packet(
                real(Path("fusion_synthesis") / "data" / "characters" / "kino.json"),
                real(CHARACTER_DIR / "ilse_marrow.json"),
                real(REQUIREMENTS_PATH),
                real(SCHEMA_PATH),
            )

    def test_a_folder_is_rejected_in_every_position(self):
        good = dict(a=real(CHARACTER_DIR / "ilse_marrow.json"), b=real(CHARACTER_DIR / "sable_quillon.json"),
                    r=real(REQUIREMENTS_PATH), s=real(SCHEMA_PATH))
        folders = (real(CHARACTER_DIR), real(Path("dev_data") / "prop001"), real(Path("proposer") / "inputs"),
                   real(Path("fusion_synthesis")))
        for position in ("a", "b", "r", "s"):
            for folder in folders:
                with self.subTest(position=position, folder=folder.name):
                    args = dict(good, **{position: folder})
                    with self.assertRaises(PacketInputError):
                        build_packet(args["a"], args["b"], args["r"], args["s"])

    def test_the_same_character_twice_is_rejected(self):
        with self.assertRaises(PacketInputError):
            build_real("ilse_marrow", "ilse_marrow")

    def test_any_other_requirements_file_is_rejected(self):
        for other in (REPO_ROOT / "README.md", REPO_ROOT / "CLAUDE.md", real(CHARACTER_DIR / "ilse_marrow.json")):
            with self.subTest(other=other.name):
                with self.assertRaises(PacketInputError):
                    build_packet(real(CHARACTER_DIR / "ilse_marrow.json"), real(CHARACTER_DIR / "sable_quillon.json"),
                                 other, real(SCHEMA_PATH))

    def test_any_other_schema_reference_is_rejected(self):
        for other in (real(Path("fusion_synthesis") / "loader.py"), real(Path("fusion_synthesis") / "render.py"),
                      real(Path("fusion_synthesis") / "data" / "pairs" / "kino__vash.json")):
            with self.subTest(other=other.name):
                with self.assertRaises(PacketInputError):
                    build_packet(real(CHARACTER_DIR / "ilse_marrow.json"), real(CHARACTER_DIR / "sable_quillon.json"),
                                 real(REQUIREMENTS_PATH), other)

    def test_a_missing_path_is_rejected(self):
        with self.assertRaises(PacketInputError):
            build_packet(real(CHARACTER_DIR / "no_such.json"), real(CHARACTER_DIR / "sable_quillon.json"),
                         real(REQUIREMENTS_PATH), real(SCHEMA_PATH))

    def test_the_permitted_requirements_path_is_rejected_if_it_holds_the_appendix(self):
        path = self.root / REQUIREMENTS_PATH
        path.write_text(path.read_text(encoding="utf-8") + "\n## Reviewer appendix (not given to the proposer)\n",
                        encoding="utf-8", newline="\n")
        with self.assertRaises(PacketInputError):
            self.build()

    def test_a_requirements_file_that_does_not_start_at_section_1_is_rejected(self):
        path = self.root / REQUIREMENTS_PATH
        path.write_text("# REQ-001\n\n" + path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        with self.assertRaises(PacketInputError):
            self.build()


class UnauthorizedFileTests(TempRoot):
    """A stray file in the development folder cannot change a packet and cannot be fed to one."""

    def stray_files(self):
        chars = self.root / CHARACTER_DIR
        shutil.copy(chars / "ilse_marrow.json", chars / "ilse_marrow_notes.json")  # innocuous name, valid card text
        shutil.copy(chars / "sable_quillon.json", chars / "tamsin_vey_v2.json")
        (chars / "readme.txt").write_text("notes\n", encoding="utf-8", newline="\n")
        (chars / "scratch.json").write_text("{}\n", encoding="utf-8", newline="\n")
        pairs = self.root / "dev_data" / "prop001" / "pairs"
        (pairs / "ilse_marrow__sable_quillon.json").write_text('{"schema": "fusion-synthesis-pair/1"}\n', encoding="utf-8", newline="\n")
        (self.root / "dev_data" / "prop001" / "extra.md").write_text("extra\n", encoding="utf-8", newline="\n")
        return [chars / "ilse_marrow_notes.json", chars / "tamsin_vey_v2.json", chars / "readme.txt", chars / "scratch.json"]

    def test_adding_unauthorized_files_does_not_change_the_packet(self):
        before = self.build()
        self.stray_files()
        after = self.build()
        self.assertEqual(before.canonical_bytes, after.canonical_bytes)
        self.assertEqual(before.packet_sha256, after.packet_sha256)

    def test_an_unauthorized_file_cannot_be_used_as_a_character(self):
        for stray in self.stray_files():
            with self.subTest(stray=stray.name):
                with self.assertRaises(PacketInputError):
                    build_packet(stray, self.root / CHARACTER_DIR / "sable_quillon.json",
                                 self.root / REQUIREMENTS_PATH, self.root / SCHEMA_PATH, repo_root=self.root)

    def test_a_permitted_name_holding_a_different_character_is_rejected(self):
        chars = self.root / CHARACTER_DIR
        (chars / "pell_dunmore.json").write_bytes((chars / "ilse_marrow.json").read_bytes())
        with self.assertRaises(PacketInputError):
            self.build("pell_dunmore", "sable_quillon")

    def test_a_permitted_name_outside_the_development_folder_is_rejected(self):
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        shutil.copy(self.root / CHARACTER_DIR / "ilse_marrow.json", elsewhere / "ilse_marrow.json")
        with self.assertRaises(PacketInputError):
            build_packet(elsewhere / "ilse_marrow.json", self.root / CHARACTER_DIR / "sable_quillon.json",
                         self.root / REQUIREMENTS_PATH, self.root / SCHEMA_PATH, repo_root=self.root)


class LeakageRegressionTests(unittest.TestCase):
    """The packet carries no authored pair content and none of the registered character names."""

    def packets(self):
        names = ("ilse_marrow", "sable_quillon", "tamsin_vey", "pell_dunmore")
        return [build_real(a, b) for a in names for b in names if a != b]

    def test_no_registered_character_name_appears_in_any_packet(self):
        for packet in self.packets():
            text = packet.canonical_bytes.decode("utf-8").lower()
            for needle in REGISTERED_NAMES + REGISTERED_SLUGS:
                with self.subTest(needle=needle):
                    self.assertNotIn(needle.lower(), text)

    def test_no_authored_pair_content_appears_in_any_packet(self):
        library = load_library()
        self.assertEqual(len(library.pairs), 5)
        needles = set()
        for pair in library.pairs:
            needles |= {pair.fusion_name, pair.emergent.name, pair.slug}
            raw = json.loads((REPO_ROOT / "fusion_synthesis" / "data" / "pairs" / f"{pair.slug}.json").read_text(encoding="utf-8"))
            stack = [raw]
            while stack:
                item = stack.pop()
                if isinstance(item, str) and len(item) >= 25:
                    needles.add(item)
                elif isinstance(item, dict):
                    stack.extend(item.values())
                elif isinstance(item, list):
                    stack.extend(item)
        self.assertGreater(len(needles), 15)
        for packet in self.packets():
            text = packet.canonical_bytes.decode("utf-8").lower()
            for needle in needles:
                with self.subTest(needle=needle[:40]):
                    self.assertNotIn(needle.lower(), text)

    def test_the_packet_embeds_no_golden_snapshot_and_no_pair_file(self):
        for packet in self.packets():
            paths = [c["path"] for c in packet.data["characters"]]
            paths += [packet.data["requirements"]["path"], packet.data["pair_schema_reference"]["path"]]
            for path in paths:
                self.assertNotIn("/pairs/", path)
                self.assertNotIn("/golden/", path)


class DeterminismTests(TempRoot):
    def test_identical_inputs_give_an_identical_hash(self):
        a, b = build_real(), build_real()
        self.assertEqual(a.canonical_bytes, b.canonical_bytes)
        self.assertEqual(a.packet_sha256, b.packet_sha256)

    def test_the_hash_is_the_sha256_of_the_canonical_bytes(self):
        packet = build_real()
        self.assertEqual(packet.packet_sha256, hashlib.sha256(packet.canonical_bytes).hexdigest())
        self.assertEqual(len(packet.packet_sha256), 64)

    def test_the_serialization_is_canonical(self):
        raw = build_real().canonical_bytes
        text = raw.decode("utf-8")
        parsed = json.loads(text)
        self.assertEqual(text, json.dumps(parsed, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
        self.assertNotIn("\r", text)
        self.assertNotIn("\n", text)  # real newlines are escaped inside the JSON strings
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))

    def test_different_character_pairs_give_different_hashes(self):
        self.assertNotEqual(build_real("ilse_marrow", "sable_quillon").packet_sha256,
                            build_real("ilse_marrow", "tamsin_vey").packet_sha256)

    def test_the_order_of_the_two_characters_is_part_of_the_packet(self):
        self.assertNotEqual(build_real("ilse_marrow", "sable_quillon").packet_sha256,
                            build_real("sable_quillon", "ilse_marrow").packet_sha256)

    def test_the_hash_does_not_depend_on_where_the_repository_sits(self):
        self.assertEqual(self.build().packet_sha256, build_real().packet_sha256)

    def test_crlf_checkouts_give_the_same_hash(self):
        expected = self.build().packet_sha256
        for rel in (CHARACTER_DIR / "ilse_marrow.json", CHARACTER_DIR / "sable_quillon.json", REQUIREMENTS_PATH, SCHEMA_PATH):
            path = self.root / rel
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(self.build().packet_sha256, expected)

    def test_a_content_change_changes_the_hash(self):
        expected = self.build().packet_sha256
        path = self.root / REQUIREMENTS_PATH
        path.write_bytes(path.read_bytes() + b"x\n")
        self.assertNotEqual(self.build().packet_sha256, expected)

    def build(self, a="ilse_marrow", b="sable_quillon"):
        return build_packet(
            self.root / CHARACTER_DIR / f"{a}.json",
            self.root / CHARACTER_DIR / f"{b}.json",
            self.root / REQUIREMENTS_PATH,
            self.root / SCHEMA_PATH,
            repo_root=self.root,
        )


if __name__ == "__main__":
    unittest.main()
