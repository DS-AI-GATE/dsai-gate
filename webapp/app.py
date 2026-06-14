"""Flask development server for the DSAI-GATE syllabus explorer."""

from pathlib import Path

from flask import Flask, jsonify, render_template

from webapp.content import MarkdownCurriculumRenderer, PAGES_URL, REPOSITORY_URL


ROOT = Path(__file__).resolve().parents[1]


def create_app(renderer=None):
    app = Flask(__name__)
    renderer = renderer or MarkdownCurriculumRenderer(ROOT)

    @app.get("/")
    def index():
        curriculum = renderer.render()
        return render_template(
            "index.html",
            **curriculum,
            repository_url=REPOSITORY_URL,
            pages_url=PAGES_URL,
        )

    @app.get("/api/syllabus")
    def syllabus():
        return jsonify(renderer.render())

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
