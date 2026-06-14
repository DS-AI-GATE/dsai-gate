# Repository Agent Guide

This document defines how maintainers and automated agents should update the
DSAI-GATE repository.

## Mission

Keep the repository accurate, syllabus-aligned, legally shareable, and useful
for learners preparing for the GATE Data Science and Artificial Intelligence
(DA) paper.

## Source Policy

Use sources in this order:

1. Official GATE organizing-institute pages for the syllabus, paper pattern,
   master question papers, and answer keys.
2. Official university, NPTEL, textbook-author, publisher, or project pages.
3. Reputable secondary resources only when an equivalent primary source is not
   available.

Do not add links to unauthorized textbook PDFs. Link to the publisher, author,
or an explicitly open-access edition instead.

Do not remove, replace, or claim to override a third party's license. Vendor
collaborator material only with explicit permission and preserve its
attribution. Otherwise, use an external link and create original adaptations.

## Required Workflow

Before changing educational content:

1. Check the current official DA syllabus.
2. Identify the exact syllabus item served by the change.
3. Prefer a focused example, exercise, or notebook over a broad content dump.
4. Verify every new external link and every local file reference.
5. Run notebooks from a clean kernel and remove accidental output or secrets.
6. Run the available repository checks before opening a pull request.

When adding an official previous-year paper, update `PYQ/README.md` and
`PYQ/SHA256SUMS`.

## Pull Request Policy

Every repository change must be proposed and merged through a pull request.
Direct pushes or commits to the default branch are not permitted, including
changes made by maintainers and automated agents.

For every change:

1. Create or use a dedicated branch.
2. Keep the pull request focused on one related set of changes.
3. Describe the purpose, affected syllabus topics, sources, and validation.
4. Wait for required automated checks and reviewer approvals.
5. Merge only after all blocking feedback is resolved.

Urgent fixes must still use a pull request. When normal review cannot happen
before an emergency merge, document the reason in the pull request and request
follow-up review immediately afterward.

Repository administrators should enforce this policy with branch protection
or a ruleset that requires pull requests and passing status checks before
changes can reach the default branch.

## Notebook Standards

Every notebook should:

- State its syllabus mapping and learning objectives at the top.
- Use a small deterministic example and set random seeds where applicable.
- Explain the concept before relying on a library implementation.
- Include at least one GATE-style MCQ, MSQ, or NAT exercise.
- Include the answer and a short explanation in a collapsible or clearly
  separated solution section.
- Avoid network downloads unless they are essential and pinned to a trusted
  source.
- Run on a standard Python scientific stack: NumPy, pandas, SciPy,
  Matplotlib, and scikit-learn.

## Link Maintenance

- Prefer HTTPS.
- Prefer stable course landing pages over semester-specific deep links.
- Every pull request automatically checks newly added Markdown, HTML, and bare
  external links, and rejects newly broken local paths.
- Record confirmed failures in `docs/stale-links.md`.
- Treat `403` and `429` results as requiring manual review; they are not always
  dead links.
- Replace repurposed domains immediately, even when they still return `200`.
- Do not silently remove a resource. Record the reason and replacement.

## Generated Subject Diagrams

Subject README files contain GitHub-rendered Mermaid concept maps between
`subject-diagram` markers. Edit the subject configuration in
`scripts/generate_subject_diagrams.py`, then run:

```bash
python scripts/generate_subject_diagrams.py
```

GitHub Actions rejects pull requests when generated diagrams are stale. Keep
the maps original and use external visual educators, including 3Blue1Brown, as
references rather than copying their artwork.

## Content Review

Check mathematical notation, worked answers, and code output. For question
analysis, use official master papers and answer keys rather than recalled or
coaching-site versions.

Reject changes that:

- Expand beyond the official syllabus without clearly labeling enrichment.
- Copy copyrighted question banks or textbooks into the repository.
- Add generated notebooks that have not been executed and reviewed.
- Introduce merge-conflict markers, broken local paths, or malformed URLs.

## Pull Request Notes

Each pull request should state:

- The syllabus topics affected.
- The official or primary sources used.
- The checks performed.
- Any link-check exceptions or known follow-up work.
