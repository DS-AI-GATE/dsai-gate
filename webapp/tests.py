"""Smoke tests for the Flask app and static export."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from webapp.app import create_app
from webapp.build import build
from webapp.content import MarkdownCurriculumRenderer, SubjectConfig


class WebappTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"GATE DA syllabus.", response.data)
        self.assertIn(b'id="resource-map"', response.data)
        self.assertIn(b'id="overall-map"', response.data)
        self.assertIn(b'id="overall-map-tab"', response.data)
        self.assertIn(b"mermaid@11.4.1", response.data)

    def test_api(self):
        response = self.client.get("/api/syllabus")
        payload = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(payload["subjects"]), 7)
        self.assertNotIn("papers", payload)
        self.assertGreater(payload["total_topics"], 40)
        self.assertGreater(payload["total_resources"], 40)
        topic_map = payload["subjects"][0]["topic_maps"][2]
        self.assertEqual(topic_map["topic"], "Conditional probability")
        self.assertIn("Probability axioms", topic_map["related"])
        self.assertTrue(
            any(resource["kind"] == "Watch" and resource["relevance"] == "topic"
                for resource in topic_map["resources"])
        )

    def test_static_export(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "site"
            build(output)
            self.assertTrue((output / "index.html").exists())
            self.assertTrue((output / "static" / "styles.css").exists())
            self.assertTrue((output / "syllabus.json").exists())
            self.assertIn(b'id="presentation"', (output / "index.html").read_bytes())
            self.assertIn(
                b"resourceMapDefinition",
                (output / "static" / "app.js").read_bytes(),
            )
            self.assertIn(
                b"overallMapDefinition",
                (output / "static" / "app.js").read_bytes(),
            )

    def test_general_markdown_renderer(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Example-Readme.md").write_text(
                "# Example-Subject\n\n"
                "```mermaid\nflowchart LR\nA[First topic] --> B[Second topic]\n```\n\n"
                "## Notes\n- [Local note](notes.md)\n- [External](https://example.com)\n",
                encoding="utf-8",
            )
            config = SubjectConfig(
                "Example-Readme.md", "example", "Example", "Example guide.", "#fff"
            )
            subject = MarkdownCurriculumRenderer(root, [config]).render()["subjects"][0]
            self.assertEqual(subject["topics"], ["First topic", "Second topic"])
            self.assertEqual(subject["topic_maps"][0]["related"], ["Second topic"])
            self.assertEqual(subject["sections"][0]["count"], 2)
            self.assertTrue(subject["sections"][0]["resources"][0]["url"].endswith("notes.md"))


if __name__ == "__main__":
    unittest.main()
