# Syllabus Explorer

The syllabus explorer is a Flask application that automatically renders the
subject Markdown guides into an interactive curriculum interface.

## Study Workspace

- **Presentation mode** turns every generated topic into a focused study slide.
- **Fullscreen mode** works from the explorer and presentation toolbar.
- **Private notes** autosave in the browser and can be exported as Markdown.
- Keyboard controls: use arrow keys to navigate, `N` for notes, `F` for
  fullscreen, and `Esc` to exit presentation mode.

Official-paper links are intentionally not attached to individual topic slides.
They should be added only after a verified topic-to-question index can open the
relevant question directly.

## Content Model

`webapp.content.MarkdownCurriculumRenderer` treats the subject Markdown files
as the source of truth:

- The first level-one heading becomes the subject title.
- Mermaid concept-map nodes become trackable syllabus topics.
- Level-two sections and their Markdown links become resource collections.
- Local links are converted to repository links for the deployed site.

To update the web application, edit the relevant subject Markdown guide and its
generated Mermaid concept map. The next build incorporates the changes
automatically.

New subject guides can be added by creating a Markdown page with the same
structure and registering its display metadata in `webapp/content.py`.

## Local Development

Install the small Flask dependency set:

```bash
python -m pip install -r webapp/requirements.txt
```

Run the development server:

```bash
python -m webapp.app
```

Then open `http://127.0.0.1:5000/`.

## Static Export

GitHub Pages cannot run a Flask server, so the same Flask template and rendered
content model are exported as a static site:

```bash
python -m webapp.build --output _site
```

The export includes `index.html`, static assets, and `syllabus.json`.

Presentation mode can be linked directly with a hash such as `#present=0`.
The complete syllabus memory map can be opened directly with `#map`.

## Deployment

`.github/workflows/pages.yml` tests and builds the application for pull
requests. After changes merge to `main`, it uploads the static export and
deploys it through GitHub Pages.

Repository administrators must set the Pages publishing source to **GitHub
Actions** once. The expected project URL is:

<https://kunaldargan.github.io/dsai-gate/>

This project URL is derived from the GitHub owner `Kunaldargan` and repository
name `dsai-gate`. A root user Pages URL would require a separate repository
named `Kunaldargan.github.io`.
