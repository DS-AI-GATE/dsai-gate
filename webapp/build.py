"""Export the Flask syllabus explorer as a GitHub Pages static site."""

from argparse import ArgumentParser
from pathlib import Path
import json
import shutil

from webapp.app import create_app
from webapp.content import MarkdownCurriculumRenderer


ROOT = Path(__file__).resolve().parents[1]
WEBAPP = ROOT / "webapp"


def build(output):
    output = output.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    renderer = MarkdownCurriculumRenderer(ROOT)
    curriculum = renderer.render()
    app = create_app(renderer)
    with app.test_client() as client:
        response = client.get("/")
        if response.status_code != 200:
            raise RuntimeError(f"Homepage export failed: HTTP {response.status_code}")
        (output / "index.html").write_bytes(response.data)

    shutil.copytree(WEBAPP / "static", output / "static")
    (output / "syllabus.json").write_text(
        json.dumps(curriculum, indent=2) + "\n",
        encoding="utf-8",
    )
    (output / ".nojekyll").touch()
    print(f"Built GitHub Pages site at {output}")


def main():
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    build(args.output)


if __name__ == "__main__":
    main()
