"""The three copies of `slug` agree, on every film there is.

A film's one name in slides/, film/ and fly/ is its slug. The rule is
written in film/ffilm/timeline.py `slug` (the owner); slides
(aimanim/film.py `slug`) and fly (library/rigs/fly.py `slugify`) keep
copies because each stage runs in its own Python (decision in
film/docs/plans/2026-10-07/UNIFY.md: no shared package). A copy that
drifts would file a film under a second name; this fails first.
The other two are read as text and run here: no film or fly code imported."""
import ast
import re
import unicodedata
import unittest
from pathlib import Path

from aimanim import film

REPO = Path(__file__).resolve().parents[2]
COPIES = {"film": (REPO / "film" / "ffilm" / "timeline.py", "slug"),
          "fly": (REPO / "fly" / "library" / "rigs" / "fly.py", "slugify")}
HARD = ["It Reads Us - We Can't Read It", "Frankfurt School vs Kołakowski Emancipation and Domination",
        "ŁÓDŹ  café — 95 %", "", "---", "Zażółć gęślą jaźń"]


def load_copy(path: Path, name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    fn.returns = None
    for a in fn.args.args:
        a.annotation = None
    space = {"re": re, "unicodedata": unicodedata}
    exec(compile(ast.Module([fn], []), str(path), "exec"), space)
    return space[name]


def names_on_disk() -> list[str]:
    found = set()
    for base in (REPO / "projects", REPO / "film" / "projects", REPO / "fly" / "projects"):
        if base.is_dir():
            found |= {p.name for p in base.iterdir() if p.is_dir()}
    return sorted(found)


class TheThreeSlugCopiesAgree(unittest.TestCase):

    def test_every_copy_gives_the_owners_answer(self):
        owner = load_copy(*COPIES["film"])
        fly = load_copy(*COPIES["fly"])
        names = names_on_disk() + HARD
        self.assertGreater(len(names), len(HARD))
        for n in names:
            with self.subTest(n):
                self.assertEqual(film.slug(n), owner(n))
                self.assertEqual(fly(n), owner(n))


if __name__ == "__main__":
    unittest.main()
