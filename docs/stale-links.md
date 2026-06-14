# Stale Link Audit

Audit date: 2026-06-11

This is the initial targeted audit of links that were insecure, malformed,
unstable, or visibly outdated. Automated checks should extend this list.

## Confirmed Problems And Remediation

| Previous URL or reference | Problem | Remediation |
| --- | --- | --- |
| `http://makeapullrequest.com` | Domain is repurposed and now contains unrelated promotional content | Point the PR badge to this repository's pull-request page |
| `http://www.uoitc.edu.iq/.../Database_Systems.pdf` | Host account is suspended and returns a 403 page | Replace with the official Pearson textbook page |
| `http://ai.berkeley.edu/section_handouts.html` | Old handout page is unavailable | Replace with the stable Berkeley CS188 open textbook |
| `http://openclassroom.stanford.edu/.../ra-exercises.html` | Legacy Stanford course path is unavailable | Replace with the stable Stanford CS145 course landing page |
| `https://arxiv.org/pdf/1502.03167.pdf%20http://...` | Two URLs were accidentally combined into one malformed URL | Use the canonical arXiv abstract URL |
| `https://arxiv.org/pdf/1609.04836.pdf,` | Trailing comma makes the URL malformed | Use the canonical arXiv abstract URL |
| `/Data/Machine-Learning/final2022_solutions.pdf` | Local file does not exist | Link to the available `final2022.pdf` paper |
| `http://noiselab.ucsd.edu/ECE228/Murphy_Machine_Learning.pdf` | Third-party book mirror returns 404 | Replace with Kevin Murphy's official Probabilistic Machine Learning page |
| `https://archive.nptel.ac.in/courses/106/106/106106145/` | Legacy archive path returns 404 | Replace with the current NPTEL course page |
| `https://github.com/chiphuyen/mlops-interview-questions` | Repository is unavailable | Replace with Chip Huyen's maintained MLOps guide |
| `https://github.com/eugeneyan/ml-test-score` | Repository is unavailable | Replace with the official Google Research publication page |

## HTTPS Upgrades

These resources still resolve but should use HTTPS:

- William Chen's probability cheatsheet.
- Artificial Intelligence: A Modern Approach official site.

## Manual Review Queue

The following categories need a broader content review even when their links
respond:

- Third-party or personal mirrors of copyrighted textbooks.
- Semester-specific course pages that have stable official landing pages.
- Deep links to university-hosted PDFs with no surrounding course context.
- Links that return `403` or `429` only to automated clients.
- Secondary practice sites presented as if they were official GATE resources.

## Ongoing Check

The repository link-check workflow should run for pull requests, manual
dispatches, and on a weekly schedule. Confirmed false positives should be
documented rather than broadly excluded.
