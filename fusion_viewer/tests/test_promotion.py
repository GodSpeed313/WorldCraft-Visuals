"""Authored fusion promotion (AUTH-019): a character file may record the authored fusion pair it was written from.

Every fixture is synthetic and built at run time in temporary folders OUTSIDE the repository: the first-generation
trio is a renamed copy of a real authored pair (as in AUTH-018's tests), the promoted profile is generated from that
pair's own data, and the second-generation pair is a plain generated filler. No private file is read by any test, and
no authored name is typed into this file.

What the origin check shows is limited, and these tests pin that: it compares the seven appearance slots and the
ability's name and description, word for word. It does not show complete inheritance fidelity."""

import hashlib
import json
import re
import unittest
from unittest import mock

from fusion_synthesis.loader import DATA_DIR, load_library
from fusion_synthesis.schema import CHARACTER_SCHEMA, PAIR_SCHEMA, character_denylist, parse_character, slugify

from fusion_viewer import character_check
from fusion_viewer.character_check import check_files, load_view
from fusion_viewer.viewmodel import EXTERNAL_AUTHORED_TEXT, build_view, resolve

from . import run_harness
from . import test_external_pairs as ep
from .test_original_characters import BASELINE_BYTES, BASELINE_SHA256, run_build, run_check

SLOTS = ("build", "face", "hair", "clothing", "palette", "signature_element", "ability_manifestation")
NEW_FUSION = ep.NEW_FUSION

# A --characters-dir build of the synthetic trio alone, taken at the AUTH-019 base (2e0705c) before any change.
TRIO_BUILD_SHA256 = "446c3ff2d139cc353e3b8b263bbb59f1b87eea7184931b5efd2c06926f246200"
TRIO_BUILD_BYTES = 202723

GEN2_FUSION = "Cinder Orchard"
GEN2_ABILITY = "Hollow Almanac"
GEN2_ABILITY_TEXT = "a plain test ability description"

# Pinned on purpose: the viewer's own constant is not trusted to define its own wording.
SENTENCE = (
    'Parent "{name}" is recorded from the authored fusion pair {slug}. The profile\'s seven appearance slots and its '
    "ability's name and description match that card word for word; nothing else in the profile is compared with it."
)
FORBIDDEN_WORDS = ("inherit", "faithful", "fidelity", "complete", "accurate", "derived")
OK_LINE = (
    "OK: {file} (ownership: not recorded; a self-declaration, not verified; origin: recorded from pair {slug}; "
    "only the seven appearance slots and the ability name and description were compared)"
)


def promoted_profile(pair_data, origin_slug, **override):
    """A character profile written from one pair file's own data: its name, its ability, its seven slots."""
    name = pair_data["fusion_name"]
    slug = slugify(name)
    ability = pair_data["emergent_ability"]
    data = {
        "schema": CHARACTER_SCHEMA,
        "name": name,
        "epistemic_status": "FICTIONAL",
        "properties": [
            {"id": f"{slug}.ability", "name": ability["name"], "description": ability["description"],
             "contribution_type": "ABILITY", "architectural_placement": "CORE_MECHANISM"},
        ],
        "visual_traits": [
            {"id": f"{slug}.v_{s}", "slot": s, "descriptor": pair_data["visual"]["slots"][s]["descriptor"], "derives_from": []}
            for s in SLOTS
        ],
        "proper_nouns": [name],
        "exclusion_candidates": [],
        "fusion_origin": {"pair": origin_slug},
    }
    data.update(override)
    return data


def second_generation_pair(a, b, fusion_name=GEN2_FUSION, ability=GEN2_ABILITY):
    """A plain filler pair between two character dicts. Its seven slots reuse a's descriptors word for word."""
    slug = f"{slugify(a['name'])}__{slugify(b['name'])}"
    eid, iid = f"{slug}.new_ability", f"{slug}.new_rule"
    a_ids, b_ids = [p["id"] for p in a["properties"]], [p["id"] for p in b["properties"]]
    scene = lambda text: {"descriptor": text, "origin": "new", "parent_ids": [eid]}  # noqa: E731
    return {
        "schema": PAIR_SCHEMA, "a": a["name"], "b": b["name"], "dominance": 50,
        "fusion_name": fusion_name, "concept": "a plain test concept",
        "interaction": {"id": iid, "description": "a plain test rule", "dependency_ids": [a_ids[0], b_ids[0]],
                        "provenance": "INVENTED_BRIDGE", "is_disclosed_modification": False},
        "emergent_ability": {"id": eid, "name": ability, "description": GEN2_ABILITY_TEXT,
                             "direct_ancestor_ids": [a_ids[0], b_ids[0]], "contribution_type": "ABILITY",
                             "architectural_placement": "EMERGENT_PROPERTY", "limitations": ["a plain test limitation"],
                             "activation": None},
        "trait_outcomes": [{"property_id": i, "outcome": "inherited", "result_text": "carried as written"} for i in a_ids + b_ids],
        "exclusions": [],
        "visual": {
            "subject": scene("a still figure"),
            "slots": {t["slot"]: {"descriptor": t["descriptor"], "origin": "A", "parent_ids": [t["id"]]} for t in a["visual_traits"]},
            "setting": scene("an empty road at dusk"), "mood": scene("calm"), "lighting": scene("low light"),
            "style": scene("painterly concept art"), "parameters": "--ar 2:3",
        },
    }


def pair_file_name(pair_data):
    return f"{slugify(pair_data['a'])}__{slugify(pair_data['b'])}.json"


class PromotionBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()
        cls.trio = ep.renamed_trio(cls.library)
        cls.gen1_pair = json.loads(cls.trio[2][1])
        cls.gen1_slug = cls.trio[2][0][: -len(".json")]
        cls.parent_a, cls.parent_b = json.loads(cls.trio[0][1]), json.loads(cls.trio[1][1])
        first = cls.library.pairs[0]
        cls.other = next(
            json.loads((DATA_DIR / "characters" / f"{c.slug}.json").read_text(encoding="utf-8"))
            for c in cls.library.characters.values() if c.name not in (first.a, first.b)
        )

    def setUp(self):
        self.folder = ep.Folder(self)

    def put(self, name, data, folder=None):
        return (folder or self.folder).write(name, json.dumps(data, indent=2))

    def profile(self, **override):
        return promoted_profile(self.gen1_pair, self.gen1_slug, **override)

    def write_trio(self):
        return [self.folder.write(name, text) for name, text in self.trio]

    def write_profile(self, data=None, folder=None):
        data = data or self.profile()
        return self.put(f"{slugify(data['name'])}.json", data, folder)

    def gen2_data(self, profile=None, **kw):
        return second_generation_pair(profile or self.profile(), self.other, **kw)

    def write_gen2(self, profile=None, **kw):
        data = self.gen2_data(profile, **kw)
        return self.put(pair_file_name(data), data)

    def write_all(self):
        """gen-1 trio, the promoted profile and the second-generation pair, as a list of paths."""
        return self.write_trio() + [self.write_profile(), self.write_gen2()]

    def paths(self):
        return sorted(self.folder.path.glob("*.json"))

    def alone_passes(self, path):
        item = character_check._prepare(path)
        self.assertNotIsInstance(item, str, item)
        self.assertIsNone(character_check._load([item]), "the file must pass on its own for this test to mean anything")


class ShapeTests(PromotionBase):
    """R1: the field is an object with exactly one key, `pair`, a non-empty string."""

    def test_each_bad_shape_is_refused_naming_the_file(self):
        cases = {
            "a list": [], "a string": "x", "null": None, "an empty object": {}, "no pair key": {"other": "x"},
            "an extra key": {"pair": "a__b", "extra": 1}, "an empty pair": {"pair": ""}, "a blank pair": {"pair": "  "},
            "a number": {"pair": 3}, "a list pair": {"pair": ["a__b"]},
        }
        for label, value in cases.items():
            with self.subTest(label):
                path = self.write_profile(self.profile(fusion_origin=value))
                result = check_files([path])
                self.assertEqual(len(result.errors), 1, result.errors)
                self.assertIn(path.name, result.errors[0])
                self.assertIn("fusion_origin", result.errors[0])
                self.assertNotIn(": origin:", result.errors[0])  # a shape error is not an origin-verification error
                self.assertEqual(result.files, ())

    def test_the_field_is_read_only_in_a_character_file(self):
        a, b, pair = self.write_trio()
        data = json.loads(pair.read_text(encoding="utf-8"))
        data["fusion_origin"] = {"pair": self.gen1_slug}
        self.put(pair.name, data)
        result = check_files([a, b, pair])
        self.assertTrue(any(pair.name in e and "fusion_origin" in e for e in result.errors), result.errors)


class StripTests(PromotionBase):
    """R2: removed from the staged copy together with `ownership`; the source file is never modified."""

    def test_the_staged_copy_has_no_fusion_origin_and_the_source_is_untouched(self):
        paths = self.write_all()
        before = self.folder.snapshot()
        result = check_files(paths)
        self.assertEqual(result.errors, ())
        item = next(i for i in result.files if i.path.name == f"{slugify(NEW_FUSION)}.json")
        self.assertEqual(item.origin, self.gen1_slug)
        self.assertNotIn(b"fusion_origin", item.staged)
        self.assertEqual(json.loads(item.staged), {k: v for k, v in self.profile().items() if k != "fusion_origin"})
        load_view(paths)
        self.assertEqual(self.folder.snapshot(), before)

    def test_ownership_and_fusion_origin_are_both_removed_and_both_kept(self):
        path = self.write_profile(self.profile(ownership="original"))
        result = check_files(self.write_trio() + [path])
        self.assertEqual(result.errors, ())
        item = next(i for i in result.files if i.path == path)
        self.assertEqual((item.ownership, item.origin), ("original", self.gen1_slug))
        self.assertNotIn(b"ownership", item.staged)
        self.assertNotIn(b"fusion_origin", item.staged)

    def test_the_loader_still_rejects_an_unknown_key_anywhere_else(self):
        path = self.write_profile(self.profile(favourite_colour="green"))
        result = check_files(self.write_trio() + [path])
        self.assertTrue(any("favourite_colour" in e for e in result.errors), result.errors)


class PromotionTests(PromotionBase):
    """AC4, AC5: a valid profile becomes a character; an unpromoted fusion does not."""

    def test_a_valid_profile_passes_and_the_second_generation_pair_resolves_in_both_orders(self):
        paths = self.write_all()
        self.assertEqual(check_files(paths).errors, ())
        view = load_view(paths)
        self.assertIn(NEW_FUSION, [c["name"] for c in view["characters"]])
        other = self.other["name"]
        forward, backward = resolve(view, NEW_FUSION, other), resolve(view, other, NEW_FUSION)
        self.assertIsNotNone(forward)
        self.assertEqual(forward["card"]["fusion_name"], GEN2_FUSION)
        self.assertEqual(forward["key"], backward["key"])
        self.assertIsNotNone(resolve(view, self.parent_a["name"], self.parent_b["name"]))  # the origin card is still there

    def test_a_fusion_with_no_profile_stays_a_card_and_is_not_selectable(self):
        paths = self.write_trio()
        view = load_view(paths)
        names = [c["name"] for c in view["characters"]]
        self.assertNotIn(NEW_FUSION, names)
        self.assertNotIn(slugify(NEW_FUSION), view["lookup"])
        self.assertTrue(all(slugify(NEW_FUSION) not in (c["a"], c["b"]) for c in view["combinations"]))
        self.assertEqual(view["pairs"][self.gen1_slug_key()]["card"]["fusion_name"], NEW_FUSION)

    def gen1_slug_key(self):
        first, second = sorted((slugify(self.parent_a["name"]), slugify(self.parent_b["name"])))
        return f"{first}__{second}"

    def test_the_origin_may_be_a_repository_pair(self):
        repo = self.library.pairs[1]
        data = json.loads((DATA_DIR / "pairs" / f"{repo.slug}.json").read_text(encoding="utf-8"))
        path = self.write_profile(promoted_profile(data, repo.slug))
        self.assertEqual(check_files([path]).errors, ())


class OriginStageTests(PromotionBase):
    """R3, R4: origin verification against the complete staged library, never during per-file validation."""

    def test_a_profile_that_passes_alone_fails_when_its_origin_pair_is_absent(self):
        profile = self.write_profile()
        self.alone_passes(profile)
        for label, paths in {"with its parents": [*self.write_trio()[:2], profile], "by itself": [profile]}.items():
            with self.subTest(label):
                result = check_files(paths)
                self.assertEqual(len(result.errors), 1, result.errors)
                self.assertIn(profile.name, result.errors[0])
                self.assertIn(": origin:", result.errors[0])
                self.assertIn(self.gen1_slug, result.errors[0])
                self.assertNotIn(profile, [i.path for i in result.files])

    def test_a_profile_that_passes_alone_fails_when_its_origin_pair_is_present_but_mismatched(self):
        def renamed():
            return promoted_profile(dict(self.gen1_pair, fusion_name="Vera Tolliver Two"), self.gen1_slug)

        def slot_changed():
            data = self.profile()
            next(t for t in data["visual_traits"] if t["slot"] == "clothing")["descriptor"] = "a changed descriptor"
            return data

        def name_changed():
            data = self.profile()
            data["properties"][0]["name"] = "A Changed Ability Name"
            return data

        def text_changed():
            data = self.profile()
            data["properties"][0]["description"] = "A changed ability description."
            return data

        cases = (
            ("the name is not the fusion name", renamed, "fusion name"),
            ("one slot descriptor differs", slot_changed, "clothing"),
            ("the ability name differs", name_changed, "no property is named"),
            ("the ability description differs", text_changed, "does not carry the ability description"),
        )
        for label, make, needle in cases:
            with self.subTest(label):
                folder = ep.Folder(self)
                trio = [folder.write(n, t) for n, t in self.trio]
                profile = self.write_profile(make(), folder)
                self.alone_passes(profile)
                result = check_files(trio + [profile])
                self.assertEqual(len(result.errors), 1, result.errors)
                self.assertIn(profile.name, result.errors[0])
                self.assertIn(": origin:", result.errors[0])
                self.assertIn(needle, result.errors[0])
                self.assertNotIn(profile, [i.path for i in result.files])

    def test_verification_runs_once_after_every_load_and_sees_the_complete_library(self):
        events, seen = [], {}
        real_load, real_verify = character_check._load, character_check._verify_origins

        def spy_load(files):
            events.append("load")
            return real_load(files)

        def spy_verify(library, promoted):
            events.append("verify")
            seen["library"], seen["promoted"] = library, list(promoted)
            return real_verify(library, promoted)

        paths = self.write_all()
        with mock.patch.object(character_check, "_load", side_effect=spy_load), \
                mock.patch.object(character_check, "_verify_origins", side_effect=spy_verify):
            result = check_files(paths)
        self.assertEqual(result.errors, ())
        self.assertEqual(events.count("verify"), 1)
        self.assertEqual(events[-1], "verify")  # nothing is loaded after it
        self.assertGreater(events.count("load"), 3)  # per-file, combined and per-pair loads all came first
        library = seen["library"]
        self.assertEqual([p.path.name for p in seen["promoted"]], [f"{slugify(NEW_FUSION)}.json"])
        self.assertTrue({NEW_FUSION, self.parent_a["name"], self.parent_b["name"], self.other["name"]} <= set(library.characters))
        self.assertTrue({self.gen1_slug, pair_file_name(self.gen2_data())[: -len(".json")]} <= {p.slug for p in library.pairs})

    def test_a_profile_is_never_checked_against_a_pair_during_its_own_per_file_validation(self):
        profile = self.write_profile()
        loads = []
        real_load = character_check._load

        def spy(files):
            loads.append([item.path.name for item in files])
            return real_load(files)

        with mock.patch.object(character_check, "_load", side_effect=spy):
            result = check_files([*self.write_trio()[:2], profile])
        self.assertIn([profile.name], loads)  # it was loaded on its own...
        self.assertEqual(len(result.errors), 1)  # ...and that load did not fail: only the origin stage did
        self.assertIn(": origin:", result.errors[0])

    def test_when_a_combined_load_fails_the_origin_stage_is_not_run_and_says_so(self):
        paths = self.write_all()
        real = character_check._load

        def fake(files):
            if sum(item.kind == character_check.CHARACTER for item in files) >= 2:
                return "a made-up clash"
            return real(files)

        with mock.patch.object(character_check, "_load", side_effect=fake), \
                mock.patch.object(character_check, "_verify_origins") as verify:
            result = check_files(paths)
        verify.assert_not_called()
        profile_name = f"{slugify(NEW_FUSION)}.json"
        self.assertTrue(any(profile_name in e and "origin not checked" in e for e in result.errors), result.errors)

    def test_when_a_combined_pair_load_fails_the_origin_stage_is_not_run_and_says_so(self):
        """The mirror of the test above. There the characters clash together; here the characters all load together
        and only the pair files clash, so `pairs_conflict` is the only thing that blocks the origin stage."""
        paths = self.write_all()
        real = character_check._load

        def fake(files):
            if sum(item.kind == character_check.PAIR for item in files) >= 2:
                return "a made-up pair clash"
            return real(files)

        profile_name = f"{slugify(NEW_FUSION)}.json"
        with mock.patch.object(character_check, "_load", side_effect=fake), \
                mock.patch.object(character_check, "_verify_origins") as verify:
            result = check_files(paths)
            code, out, _err = run_check(*paths)
        verify.assert_not_called()
        self.assertTrue(any("conflict between" in e and "a made-up pair clash" in e for e in result.errors), result.errors)
        self.assertFalse(any("conflict between" in e and "a made-up pair clash" not in e for e in result.errors), result.errors)
        self.assertTrue(any(profile_name in e and "origin not checked" in e for e in result.errors), result.errors)
        self.assertNotIn(profile_name, [i.path.name for i in result.files])
        self.assertEqual(code, 2)
        self.assertNotIn(f"OK: {profile_name}", out)

    def test_two_pairs_may_share_a_fusion_name_and_the_slug_decides_which_one_is_meant(self):
        trio = self.write_trio()
        profile = self.write_profile()
        gen2 = self.write_gen2(fusion_name=NEW_FUSION)  # same fusion name as the first-generation pair
        self.assertEqual(check_files(trio + [profile, gen2]).errors, ())
        gen2_slug = gen2.name[: -len(".json")]
        wrong = self.write_profile(self.profile(fusion_origin={"pair": gen2_slug}))
        result = check_files(trio + [wrong, gen2])
        blob = "\n".join(result.errors)
        self.assertIn(gen2_slug, blob)
        self.assertIn("parent of its own origin pair", blob)
        self.assertNotIn(self.gen1_slug, blob)

    def test_two_profiles_that_would_be_the_same_character_fail_through_the_existing_collision_rule(self):
        second = ep.Folder(self)
        first_path = self.write_profile()
        second_path = self.write_profile(folder=second)
        result = check_files(self.write_trio() + [first_path, second_path])
        self.assertTrue(any("would both be" in e for e in result.errors), result.errors)


class FirstGenerationTests(PromotionBase):
    """R4 O3: slice 1 records first-generation promotions only (a check, not part of the file format)."""

    def test_a_profile_that_is_a_parent_of_its_own_origin_pair_fails(self):
        base = self.profile()
        pair = self.gen2_data(base, fusion_name=NEW_FUSION)
        slug = pair_file_name(pair)[: -len(".json")]
        ability = pair["emergent_ability"]
        profile = self.profile(fusion_origin={"pair": slug})
        profile["properties"][0].update(name=ability["name"], description=ability["description"])
        pair_path = self.put(pair_file_name(pair), pair)
        profile_path = self.write_profile(profile)
        result = check_files([profile_path, pair_path])
        self.assertEqual(len(result.errors), 1, result.errors)
        self.assertIn("parent of its own origin pair", result.errors[0])
        self.assertIn(profile_path.name, result.errors[0])

    def test_a_profile_whose_origin_pair_has_a_promoted_parent_fails_and_the_first_still_passes(self):
        paths = self.write_trio() + [self.write_profile()]
        gen2 = self.gen2_data()
        gen2_slug = pair_file_name(gen2)[: -len(".json")]
        second = promoted_profile(gen2, gen2_slug)
        paths += [self.put(pair_file_name(gen2), gen2), self.put(f"{slugify(GEN2_FUSION)}.json", second)]
        result = check_files(paths)
        self.assertEqual(len(result.errors), 1, result.errors)
        self.assertIn(f"{slugify(GEN2_FUSION)}.json", result.errors[0])
        self.assertIn("itself a promoted profile", result.errors[0])
        self.assertIn(f"{slugify(NEW_FUSION)}.json", [i.path.name for i in result.files])


class ViewerTextTests(PromotionBase):
    """R5, AC12: what the page says, and what it must not say."""

    def setUp(self):
        super().setUp()
        self.view = load_view(self.write_all())
        self.record = resolve(self.view, NEW_FUSION, self.other["name"])

    def test_the_second_generation_card_carries_exactly_the_pinned_sentence(self):
        expected = EXTERNAL_AUTHORED_TEXT + " " + SENTENCE.format(name=NEW_FUSION, slug=self.gen1_slug)
        self.assertEqual(self.record["status"]["authored"]["text"], expected)
        self.assertTrue(self.record["status"]["authored"]["source_file"].startswith(f"External folder ({ep.FOLDER_NAME})"))

    def test_the_sentence_says_recorded_from_and_what_was_compared_and_nothing_stronger(self):
        sentence = SENTENCE.format(name=NEW_FUSION, slug=self.gen1_slug).lower()
        for needle in ("recorded from", "match that card word for word", "nothing else in the profile is compared"):
            self.assertIn(needle, sentence)
        text = self.record["status"]["authored"]["text"].lower()
        for word in FORBIDDEN_WORDS:
            self.assertNotIn(word, text, word)

    def test_the_sentence_appears_in_no_other_field(self):
        rest = dict(self.record["status"], authored={k: v for k, v in self.record["status"]["authored"].items() if k != "text"})
        for part in (rest, self.record["card"], self.record["comparison"]):
            self.assertNotIn("recorded from", json.dumps(part))

    def test_the_first_generation_card_and_the_repository_cards_are_untouched(self):
        first = self.view["pairs"][self.gen1_slug_key()]
        self.assertEqual(first["status"]["authored"]["text"], EXTERNAL_AUTHORED_TEXT)
        plain = build_view()
        for key, record in plain["pairs"].items():
            with self.subTest(pair=key):
                self.assertEqual(json.dumps(self.view["pairs"][key]["status"], sort_keys=True), json.dumps(record["status"], sort_keys=True))

    def gen1_slug_key(self):
        first, second = sorted((slugify(self.parent_a["name"]), slugify(self.parent_b["name"])))
        return f"{first}__{second}"

    def test_two_promoted_parents_are_named_side_a_first_then_side_b(self):
        repo = self.library.pairs[1]
        repo_data = json.loads((DATA_DIR / "pairs" / f"{repo.slug}.json").read_text(encoding="utf-8"))
        first, second = self.profile(), promoted_profile(repo_data, repo.slug)
        for label, (a, b) in {"profile first": (first, second), "profile second": (second, first)}.items():
            with self.subTest(label):
                folder = ep.Folder(self)
                pair = second_generation_pair(a, b)
                paths = [folder.write(n, t) for n, t in self.trio]
                paths += [self.put(f"{slugify(d['name'])}.json", d, folder) for d in (first, second)]
                paths.append(self.put(pair_file_name(pair), pair, folder))
                self.assertEqual(check_files(paths).errors, ())
                record = resolve(load_view(paths), a["name"], b["name"])
                text = record["status"]["authored"]["text"]
                origin = {first["name"]: self.gen1_slug, second["name"]: repo.slug}
                tail = " ".join(SENTENCE.format(name=x["name"], slug=origin[x["name"]]) for x in (a, b))
                self.assertEqual(text, EXTERNAL_AUTHORED_TEXT + " " + tail)


class CheckerOutputTests(PromotionBase):
    """R6: the checker's line says only what was compared."""

    def test_a_passing_profile_prints_the_limited_line(self):
        code, out, err = run_check(*self.write_all())
        self.assertEqual(code, 0, err)
        line = OK_LINE.format(file=f"{slugify(NEW_FUSION)}.json", slug=self.gen1_slug)
        self.assertIn(line, out.splitlines())
        for word in FORBIDDEN_WORDS:
            self.assertNotIn(word, line.lower())

    def test_a_failing_profile_prints_no_ok_line(self):
        profile = self.write_profile(self.profile())
        code, out, err = run_check(*self.write_trio()[:2], profile)
        self.assertEqual(code, 2)
        self.assertNotIn(f"OK: {profile.name}", out)
        self.assertIn(f"ERROR: {profile.name}: origin:", err)


class BuildTests(PromotionBase):
    """The build writes nothing when the origin does not verify; the page holds no private path or golden claim."""

    def test_a_failed_origin_stops_the_build_and_writes_nothing(self):
        self.write_trio()
        self.write_profile(self.profile(properties=[dict(self.profile()["properties"][0], name="A Changed Name")]))
        out = self.folder.parent / "never.html"
        code, _o, err = run_build("--out", out, "--characters-dir", self.folder.path)
        self.assertEqual(code, 2)
        self.assertIn(": origin:", err)
        self.assertFalse(out.exists())

    def test_the_page_holds_no_absolute_local_path_and_makes_no_golden_claim(self):
        self.write_all()
        out = self.folder.parent / "viewer.html"
        code, _o, err = run_build("--out", out, "--characters-dir", self.folder.path)
        self.assertEqual(code, 0, err)
        html = out.read_text(encoding="utf-8")
        low = html.lower()
        for needle in ep.NoPrivatePathTests.forbidden(None, self.folder.path):
            self.assertNotIn(needle, low, f"page contains {needle!r}")
        self.assertIsNone(re.search(r"(?<![A-Za-z])[A-Za-z]:[\\/]", html))
        self.assertIsNone(re.search(r"(?<![A-Za-z0-9:/.])/(users|home|tmp|var|private|mnt)/", low))
        self.assertIn("recorded from the authored fusion pair", html)
        record = resolve(load_view(self.paths()), NEW_FUSION, self.other["name"])
        blob = json.dumps(record["status"]).lower()
        self.assertEqual(blob.count("golden"), 1)  # only "no operator-approved golden snapshot"
        for word in ("equals the golden", "matches the golden", "identical to the golden"):
            self.assertNotIn(word, blob)
        self.assertFalse((DATA_DIR / "golden" / pair_file_name(self.gen2_data())).exists())

    def test_the_real_page_shows_the_sentence_under_status_details_for_the_second_generation_pair_only(self):
        self.write_all()
        out = self.folder.parent / "viewer.html"
        code, _o, err = run_build("--out", out, "--characters-dir", self.folder.path)
        self.assertEqual(code, 0, err)
        snap = run_harness(out.read_text(encoding="utf-8"))  # runs the page's own script under node
        marker = "recorded from the authored fusion pair"
        shown = {(p["x"], p["y"]) for p in snap["pairs"] if marker in (p.get("detailsText") or "")}
        mine, other = slugify(NEW_FUSION), slugify(self.other["name"])
        self.assertEqual(shown, {(mine, other), (other, mine)})
        page = next(p for p in snap["pairs"] if (p["x"], p["y"]) == (mine, other))
        self.assertIn(SENTENCE.format(name=NEW_FUSION, slug=self.gen1_slug), page["detailsText"])

    def test_two_builds_of_a_promoted_folder_are_byte_identical(self):
        self.write_all()
        outs = [self.folder.parent / f"v{i}.html" for i in (1, 2)]
        for out in outs:
            code, _o, err = run_build("--out", out, "--characters-dir", self.folder.path)
            self.assertEqual(code, 0, err)
        self.assertEqual(outs[0].read_bytes(), outs[1].read_bytes())


class BaselineTests(PromotionBase):
    """R8, AC2: nothing changes unless a file carries `fusion_origin`."""

    def test_the_default_build_is_byte_identical_to_the_baseline(self):
        out = self.folder.parent / "default.html"
        code, _o, err = run_build("--out", out)
        self.assertEqual(code, 0, err)
        data = out.read_bytes()
        self.assertEqual((len(data), hashlib.sha256(data).hexdigest()), (BASELINE_BYTES, BASELINE_SHA256))

    def test_a_characters_dir_build_with_no_fusion_origin_is_byte_identical_to_the_base(self):
        self.write_trio()
        out = self.folder.parent / "trio.html"
        code, _o, err = run_build("--out", out, "--characters-dir", self.folder.path)
        self.assertEqual(code, 0, err)
        data = out.read_bytes()
        self.assertEqual((len(data), hashlib.sha256(data).hexdigest()), (TRIO_BUILD_BYTES, TRIO_BUILD_SHA256))


class GapCharacterizationTests(PromotionBase):
    """The disclosed AUTH-019 gap, pinned so that fixing it is a deliberate act and not a side effect.

    A promoted profile's denylist is its own name, property names and proper nouns as authored. Its origin parents'
    proper nouns are not added. This is a characterization of today's behaviour, not a requirement."""

    def test_a_profile_that_omits_its_origin_parents_proper_nouns_still_passes(self):
        parent_nouns = set(self.parent_a["proper_nouns"]) | set(self.parent_b["proper_nouns"])
        self.assertTrue(parent_nouns, "the fixture parents must have proper nouns for this test to mean anything")
        data = self.profile()
        self.assertEqual(check_files(self.write_all()).errors, ())
        entries = {entry for entry, _source in character_denylist(parse_character({k: v for k, v in data.items() if k != "fusion_origin"}))}
        self.assertEqual(entries & parent_nouns, set())


if __name__ == "__main__":
    unittest.main()
