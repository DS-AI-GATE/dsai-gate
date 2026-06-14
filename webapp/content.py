"""General Markdown-to-curriculum renderer for the syllabus explorer."""

from dataclasses import dataclass
from pathlib import Path
import html
import re
from typing import Optional


REPOSITORY_URL = "https://github.com/Kunaldargan/dsai-gate"
PAGES_URL = "https://kunaldargan.github.io/dsai-gate/"

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
LINK = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")
MERMAID_BLOCK = re.compile(r"```mermaid\s+(.*?)```", re.DOTALL)
MERMAID_NODE = re.compile(r"\b[A-Za-z][A-Za-z0-9_]*\[([^\]]+)\]")
MERMAID_EDGE = re.compile(
    r"\b([A-Za-z][A-Za-z0-9_]*)(?:[\[{][^\]}]+[\]}])?\s*-->"
    r"(?:\|[^|]+\|)?\s*([A-Za-z][A-Za-z0-9_]*)"
)
HTML_TAG = re.compile(r"<[^>]+>")
WORD = re.compile(r"[a-z0-9]+")
STOP_WORDS = {
    "and", "the", "for", "from", "with", "into", "course", "notes", "introduction",
    "data", "learning", "machine", "artificial", "probability", "statistics",
}


@dataclass(frozen=True)
class SubjectConfig:
    """Display metadata for one automatically rendered Markdown guide."""

    source: str
    slug: str
    short: str
    description: str
    accent: str
    notebook: Optional[str] = None


SUBJECT_CONFIGS = [
    SubjectConfig(
        "Probability-Statistics-Readme.md",
        "probability",
        "Probability",
        "Reason about uncertainty, distributions, estimation, and statistical decisions.",
        "#8b5cf6",
        "notebooks/probability/conditional_probability_and_bayes.ipynb",
    ),
    SubjectConfig(
        "Linear-Algebra-Readme.md",
        "linear-algebra",
        "Linear Algebra",
        "Build the matrix intuition behind data, optimization, and machine learning.",
        "#06b6d4",
        "notebooks/linear_algebra/projections_and_pca.ipynb",
    ),
    SubjectConfig(
        "Calculus-and-Optimization-Readme.md",
        "calculus",
        "Calculus",
        "Understand change, approximation, and the mechanics of optimization.",
        "#f59e0b",
    ),
    SubjectConfig(
        "Programming-and-Algorithms-Readme.md",
        "programming",
        "Programming",
        "Translate problems into Python programs and efficient algorithms.",
        "#22c55e",
        "notebooks/algorithms/binary_search_and_complexity.ipynb",
    ),
    SubjectConfig(
        "Database-Management-Readme.md",
        "databases",
        "Databases",
        "Model, query, organize, and analyze structured data systems.",
        "#f97316",
    ),
    SubjectConfig(
        "Machine-Learning-Readme.md",
        "machine-learning",
        "Machine Learning",
        "Connect models, objectives, validation, and data-driven decisions.",
        "#ec4899",
        "notebooks/machine_learning/linear_regression_from_scratch.ipynb",
    ),
    SubjectConfig(
        "Artificial-Intelligence-Readme.md",
        "artificial-intelligence",
        "Artificial Intelligence",
        "Explore search, logic, uncertainty, and computational reasoning.",
        "#6366f1",
    ),
]

class MarkdownCurriculumRenderer:
    """Discover and convert Markdown guides into app-ready curriculum data."""

    ignored_sections = {"interactive concept map", "table of contents"}

    def __init__(self, root, configs=None, repository_url=REPOSITORY_URL):
        self.root = Path(root).resolve()
        self.configs = configs or SUBJECT_CONFIGS
        self.repository_url = repository_url.rstrip("/")

    def render(self):
        subjects = [
            self.render_subject(config, number)
            for number, config in enumerate(self.configs, start=1)
        ]
        return {
            "subjects": subjects,
            "total_topics": sum(len(subject["topics"]) for subject in subjects),
            "total_resources": sum(
                section["count"]
                for subject in subjects
                for section in subject["sections"]
            ),
        }

    def render_subject(self, config, number):
        path = self.root / config.source
        text = path.read_text(encoding="utf-8")
        title = self._title(text) or config.short
        topics, related_topics = self._topic_graph(text)
        sections = self._sections(text, path)
        resources = self._resource_catalog(text, path, sections)

        return {
            "id": config.slug,
            "number": f"{number:02d}",
            "title": self._display_title(title),
            "short": config.short,
            "description": config.description,
            "accent": config.accent,
            "guide": self._repository_link(config.source),
            "notebook": self._repository_link(config.notebook) if config.notebook else None,
            "topics": topics,
            "topic_maps": [
                {
                    "topic": topic,
                    "related": related_topics.get(topic, []),
                    "resources": self._topic_resources(topic, resources),
                }
                for topic in topics
            ],
            "sections": sections,
            "source": config.source,
        }

    def _title(self, text):
        for line in text.splitlines():
            match = HEADING.match(line)
            if match and len(match.group(1)) == 1:
                return self._clean_text(match.group(2))
        return ""

    def _topics(self, text):
        return self._topic_graph(text)[0]

    def _topic_graph(self, text):
        block = MERMAID_BLOCK.search(text)
        if not block:
            return [], {}
        topics = []
        nodes = {}
        for raw_topic in MERMAID_NODE.findall(block.group(1)):
            topic = self._clean_text(raw_topic)
            if topic and topic not in topics:
                topics.append(topic)
        for node, raw_topic in re.findall(r"\b([A-Za-z][A-Za-z0-9_]*)[\[{]([^\]}]+)[\]}]", block.group(1)):
            nodes[node] = self._clean_text(raw_topic)

        related = {topic: [] for topic in topics}
        for source, target in MERMAID_EDGE.findall(block.group(1)):
            left, right = nodes.get(source), nodes.get(target)
            if left in related and right and right not in related[left]:
                related[left].append(right)
            if right in related and left and left not in related[right]:
                related[right].append(left)
        return topics, related

    def _resource_catalog(self, text, source_path, sections):
        resources = []
        for section in sections:
            for resource in section["resources"]:
                self._add_resource(resources, resource, section["title"], source_path.stem, "subject")

        for label, target in LINK.findall(text):
            if label.strip() and not target.strip().startswith("#"):
                self._add_resource(
                    resources,
                    {"title": self._clean_text(label), "url": self._resolve_link(target, source_path)},
                    "Concept map",
                    source_path.stem,
                    "concept",
                )

        supplemental = [
            *self.root.glob("Topic_Resources/**/*.md"),
            self.root / "notebooks" / "README.md",
            self.root / "Interview" / "ML_Fundamentals.md",
            self.root / "PYQ" / "README.md",
        ]
        for path in supplemental:
            if not path.is_file():
                continue
            supplemental_text = path.read_text(encoding="utf-8")
            for label, target in LINK.findall(supplemental_text):
                if label.strip() and not target.strip().startswith("#"):
                    self._add_resource(
                        resources,
                        {"title": self._clean_text(label), "url": self._resolve_link(target, path)},
                        "Repository resource",
                        path.stem.replace("_", " "),
                        "supplemental",
                    )
        return resources

    def _add_resource(self, resources, resource, section, context, scope):
        if not resource["title"] or not resource["url"]:
            return
        candidate = {
            **resource,
            "section": section,
            "context": self._clean_text(context),
            "kind": self._resource_kind(resource["title"], resource["url"], section),
            "scope": scope,
        }
        if not any(item["url"] == candidate["url"] for item in resources):
            resources.append(candidate)

    def _topic_resources(self, topic, resources):
        ranked = sorted(
            ((self._resource_score(topic, resource), resource) for resource in resources),
            key=lambda item: (-item[0], item[1]["title"].lower()),
        )
        selected = []
        seen_kinds = set()

        for score, resource in ranked:
            minimum_score = 20 if resource["scope"] == "supplemental" else 10
            if score < minimum_score:
                continue
            if len(selected) >= 6:
                break
            selected.append({**resource, "relevance": "topic"})
            seen_kinds.add(resource["kind"])

        for _, resource in ranked:
            if len(selected) >= 6:
                break
            if resource["scope"] != "subject" or resource["kind"] in seen_kinds or resource in selected:
                continue
            selected.append({**resource, "relevance": "subject"})
            seen_kinds.add(resource["kind"])
        return selected

    @staticmethod
    def _resource_score(topic, resource):
        topic_text = topic.lower()
        resource_text = f"{resource['title']} {resource['context']}".lower()
        if topic_text in resource_text:
            return 100
        topic_words = {word for word in WORD.findall(topic_text) if word not in STOP_WORDS and len(word) > 2}
        resource_words = set(WORD.findall(resource_text))
        return len(topic_words & resource_words) * 10

    @staticmethod
    def _resource_kind(title, url, section):
        text = f"{title} {url} {section}".lower()
        if "youtube.com" in text or "youtu.be" in text:
            return "Watch"
        if "ipynb" in text or "notebook" in text or "coding" in text:
            return "Notebook"
        if any(word in text for word in ("problem", "question", "practice", "assignment", "exercise", "pyq", "homework")):
            return "Practice"
        if any(word in text for word in ("course", "nptel", "ocw", "mooc", "cs188", "cs229", "stat110")):
            return "Course"
        return "Read"

    def _sections(self, text, source_path):
        sections = []
        current = None
        in_fence = False
        in_comment = False

        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("<!--"):
                in_comment = True
            if in_comment:
                if stripped.endswith("-->"):
                    in_comment = False
                continue
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            heading = HEADING.match(line)
            if heading and len(heading.group(1)) == 2:
                name = self._clean_text(heading.group(2))
                if name.lower() in self.ignored_sections:
                    current = None
                else:
                    current = {"title": name, "resources": [], "count": 0}
                    sections.append(current)
                continue

            if current is None:
                continue
            for label, target in LINK.findall(line):
                if (
                    not label.strip()
                    or label.lstrip().startswith("<img")
                    or target.strip().startswith("#")
                ):
                    continue
                resource = {
                    "title": self._clean_text(label),
                    "url": self._resolve_link(target, source_path),
                }
                if resource not in current["resources"]:
                    current["resources"].append(resource)

        rendered = []
        for section in sections:
            if section["resources"]:
                section["count"] = len(section["resources"])
                rendered.append(section)
        return rendered

    def _resolve_link(self, target, source_path):
        target = target.strip().strip("<>").split(" ", 1)[0]
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return target
        if target.startswith("/"):
            relative = target.lstrip("/")
        else:
            relative = (source_path.parent / target).relative_to(self.root).as_posix()
        return self._repository_link(relative)

    def _repository_link(self, relative):
        return f"{self.repository_url}/blob/main/{relative}" if relative else ""

    @staticmethod
    def _clean_text(value):
        value = HTML_TAG.sub("", value)
        value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
        value = value.replace("**", "").replace("`", "").replace("\\", "")
        return html.unescape(re.sub(r"\s+", " ", value).strip(" #-"))

    @staticmethod
    def _display_title(title):
        replacements = {
            "Probability-Statistics": "Probability & Statistics",
            "Linear-Algebra": "Linear Algebra",
            "Calculus-and-Optimization": "Calculus & Optimization",
            "Programming-And-Algorithms-Python": "Programming & Algorithms",
            "Database-Management": "Database Management",
            "Machine-Learning": "Machine Learning",
            "Artificial-Intelligence": "Artificial Intelligence",
        }
        return replacements.get(title, title.replace("-", " "))
