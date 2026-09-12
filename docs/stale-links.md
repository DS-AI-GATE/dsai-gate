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
| `https://www.cin.ufpe.br/~jrsl/Books/Linear%20Algebra%20Done%20Right%20-%20Sheldon%20Axler.pdf` | Unauthorized third-party PDF mirror | Replace with Sheldon Axler's official open-access site `https://linear.axler.net/` |
| `https://drive.google.com/file/d/1OQPTKFpc6aLWZoBOto3e7kk5jvBBZxNc/view?usp=sharing` | Personal Google Drive PDF mirror | Replace with official open-access book site `http://probabilitybook.net/` |
| `https://egrcc.github.io/docs/math/all-of-statistics.pdf` | Unauthorized third-party PDF mirror | Replace with official Springer publisher page `https://link.springer.com/book/10.1007/978-0-387-21736-9` |
| `https://github.com/aforarup/interview/.../Algorithm%20Design%20by%20Jon%20Kleinberg,%20Eva%20Tardos.pdf` | Unauthorized third-party PDF mirror | Replace with official Pearson publisher page `https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003264/9780321295354` |
| `https://openeclass.panteion.gr/.../Learning%20From%20Data...pdf` | Unauthorized third-party PDF mirror | Replace with official book landing page `https://amlbook.com/` |
| `https://www.sku.ac.ir/.../Data-Mining-Concepts-and-Techniques-Han.pdf` | Unauthorized third-party PDF mirror | Replace with official author page `https://www.cs.illinois.edu/~hanj/bk3/` |
| `https://www.cse.iitd.ac.in/~parags/teaching/col774/` | 404 Not Found semester-specific path | Replace with stable teaching landing page `https://www.cse.iitd.ac.in/~parags/teaching.html` |
| `https://ocw.mit.edu/ans7870/resources/Strang/Edited/Calculus/Calculus.pdf` | 301 Permanent Redirect | Replace with canonical course URL `https://ocw.mit.edu/courses/res-18-001-calculus-online-textbook-spring-2005/` |

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
