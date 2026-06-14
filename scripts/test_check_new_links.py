"""Regression tests for Markdown link collection."""

import unittest

from check_new_links import links_in


class LinksInTests(unittest.TestCase):
    def test_nested_badge_links_are_not_combined(self):
        line = "[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)"

        self.assertEqual(
            set(links_in(line)),
            {"https://awesome.re/badge.svg", "https://awesome.re"},
        )

    def test_inline_code_urls_are_ignored(self):
        line = "| `[dead](http://dead.example/path)` | historical reference |"

        self.assertEqual(set(links_in(line)), set())

    def test_markdown_and_bare_links_are_collected_once(self):
        line = "[Course](https://example.com/course) and https://example.org/bare."

        self.assertEqual(
            set(links_in(line)),
            {"https://example.com/course", "https://example.org/bare"},
        )


if __name__ == "__main__":
    unittest.main()
