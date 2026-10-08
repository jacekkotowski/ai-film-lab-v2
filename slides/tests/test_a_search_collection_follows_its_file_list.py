"""A search collection follows its file list.

2026-10-08: qmd's `v2` still had the file list of 2026-10-07 (it looked for
slides/films/*.script.txt, moved to projects/ that day, and had no docs/*.md),
so docs/OPEN.md and the films' slides scripts could not be found. MASK in
knowledge.py was already right: `setup` skipped a collection that existed,
and `refresh` never compared the lists. Standard library only; no qmd needed.
"""

import unittest

from aimanim import knowledge

LISTING = """Collections (3):

v2 (qmd://v2/)
  Pattern:  CLAUDE.md,slides/films/*.script.txt
  Files:    87
  Updated:  37m ago

v2-code (qmd://v2-code/)
  Pattern:  film/ffilm/**/*.py
  Files:    156
  Updated:  38m ago

v2-history (qmd://v2-history/)
  Pattern:  **/*.md
  Files:    360
  Updated:  33m ago
"""


class FileLists(unittest.TestCase):
    def test_the_file_lists_qmd_holds_are_read_from_its_listing(self):
        self.assertEqual(knowledge.patterns_of(LISTING), {
            "v2": "CLAUDE.md,slides/films/*.script.txt",
            "v2-code": "film/ffilm/**/*.py",
            "v2-history": "**/*.md"})

    def test_windows_line_ends_read_the_same(self):
        self.assertEqual(knowledge.patterns_of(LISTING.replace("\n", "\r\n")),
                         knowledge.patterns_of(LISTING))

    def test_a_missing_collection_is_added(self):
        self.assertEqual(knowledge.what_to_do("v2", "CLAUDE.md", {}), "add")

    def test_an_unchanged_collection_is_kept(self):
        self.assertEqual(knowledge.what_to_do("v2", "CLAUDE.md", {"v2": "CLAUDE.md"}), "keep")

    def test_a_collection_whose_file_list_changed_is_replaced(self):
        have = knowledge.patterns_of(LISTING)
        self.assertEqual(knowledge.what_to_do("v2", knowledge.MASK, have), "replace")

    def test_every_entry_of_the_file_lists_finds_a_file(self):
        for mask in (knowledge.MASK, knowledge.CODE_MASK):
            for entry in mask.split(","):
                self.assertTrue(any(knowledge.ROOT.glob(entry)),
                                f"{entry} finds no file: moved?")


if __name__ == "__main__":
    unittest.main()
