# DSAI-GATE Implementation Plan

Last reviewed: 2026-06-11

## Goal

Modernize the repository around the official GATE 2026 DA syllabus and the
official 2024-2026 question papers, while improving reliability and adding
focused, executable learning material.

## Evidence Base

- [Official GATE 2026 DA syllabus](https://gate2026.iitg.ac.in/doc/GATE2026_Syllabus/DA_2026_Syllabus.pdf)
- [Official GATE 2026 paper pattern](https://gate2026.iitg.ac.in/question-paper-pattern.html)
- [Official GATE 2026 DA master paper](https://gate2026.iitg.ac.in/doc/download/2026/QPs/DA.pdf)
- [Official GATE 2026 DA answer key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)
- Local official papers and keys in `PYQ/` for 2024-2026

The syllabus remains organized into seven subject areas: probability and
statistics, linear algebra, calculus and optimization, programming/data
structures/algorithms, database management and warehousing, machine learning,
and artificial intelligence.

The 2026 DA subject section contains 23 MCQs, 14 MSQs, and 18 NATs. This mix
supports adding practice that tests reasoning and calculation, not only
single-answer recall.

## Phase 1: Reliability And Documentation

- Keep maintenance policy in `docs/agent.md`.
- Maintain a dated audit in `docs/stale-links.md`.
- Add scheduled and pull-request link checking.
- Remove merge-conflict markers and malformed URLs.
- Replace unauthorized or unstable textbook links with official publisher or
  author pages.
- Add the official 2026 master paper and key to the previous-year-paper index.

Exit criteria:

- No merge-conflict markers.
- All local Markdown links resolve.
- Confirmed stale or repurposed links are removed or replaced.
- Link checking runs automatically.

## Phase 2: High-Priority Concept Notebooks

Create one compact notebook per concept. Each notebook must satisfy
`docs/agent.md`.

| Priority | Subject | Planned notebook | Syllabus and paper focus |
| --- | --- | --- | --- |
| P0 | Probability | `conditional_probability_and_bayes.ipynb` | Bayes theorem, conditional probability, diagnostic-test NATs |
| P0 | Probability | `distributions_cdf_and_expectation.ipynb` | Normal, exponential, chi-squared, CDF, expectation |
| P0 | Linear algebra | `projections_eigenvalues_and_pca.ipynb` | Projection matrices, eigenvectors, PCA |
| P0 | Algorithms | `search_sort_and_complexity.ipynb` | Binary search, quicksort recurrences, tree traversal |
| P0 | Databases | `relational_algebra_sql_and_normalization.ipynb` | Keys, constraints, SQL aggregation, normalization |
| P0 | Machine learning | `regression_regularization_and_validation.ipynb` | Ridge regression, loss, bias-variance, LOOCV |
| P0 | AI | `search_logic_and_probabilistic_inference.ipynb` | Search, logic, minimax, inference |
| P1 | Calculus | `single_variable_optimization.ipynb` | Limits, derivatives, Taylor series, extrema |
| P1 | Machine learning | `clustering_and_distance_metrics.ipynb` | k-means, k-medoid, hierarchical clustering |
| P1 | Machine learning | `mlp_parameter_counting.ipynb` | Feed-forward networks and parameter counts |
| P1 | Databases | `indexing_and_data_warehousing.ipynb` | B+ trees, OLAP, multidimensional models |
| P1 | AI | `variable_elimination_and_sampling.ipynb` | Exact and approximate inference |

Exit criteria for each notebook:

- Clean-kernel execution succeeds.
- At least three practice questions cover two or more GATE question types.
- The relevant topic README links to it.

## Phase 3: Topic Coverage And Question Bank

- Build a syllabus-to-resource matrix with one primary resource and one
  practice source per syllabus item.
- Tag official 2024-2026 DA questions by subject, concept, marks, and question
  type without reproducing copyrighted paper content.
- Add original GATE-style questions with reviewed solutions.
- Track weak-coverage areas explicitly. Initial priorities are tuple calculus,
  data warehousing computations, conditional PDF, hypothesis testing,
  approximate inference, and single-variable Taylor-series problems.

## Phase 4: Repository Presentation

- Rewrite topic README files to use a consistent structure: syllabus mapping,
  primary resources, examples, practice, and enrichment.
- Reduce decorative language and remove outdated calls to action.
- Add contribution guidelines and issue templates for stale links, notebook
  requests, and syllabus updates.
- Keep interview material separate from exam-syllabus material.

## Delivery Order

1. Reliability and official-source documentation.
2. Seven P0 notebooks, one for each syllabus area.
3. Question metadata and original practice.
4. P1 notebooks and presentation cleanup.
