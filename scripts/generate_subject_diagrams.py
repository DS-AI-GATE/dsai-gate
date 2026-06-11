"""Generate GitHub-rendered Mermaid concept maps in subject Markdown files."""

from argparse import ArgumentParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- subject-diagram:start -->"
END = "<!-- subject-diagram:end -->"

SUBJECTS = {
    "Probability-Statistics-Readme.md": {
        "title": "Probability and Statistics Concept Map",
        "graph": """
flowchart LR
    A[Counting and sample spaces] --> B[Probability axioms]
    B --> C[Conditional probability]
    C --> D[Bayes theorem]
    B --> E[Random variables]
    E --> F[PMF, PDF, and CDF]
    F --> G[Expectation and variance]
    G --> H[CLT and confidence intervals]
    H --> I[z, t, and chi-squared tests]
""",
        "reference": "Visual intuition references: [Bayes theorem](https://youtu.be/HZGCoVF3YvM) and [Central Limit Theorem](https://youtube.com/playlist?list=PLZHQObOWTQDOMxJDswBaLu8xBMKxSTvg8) by 3Blue1Brown.",
    },
    "Linear-Algebra-Readme.md": {
        "title": "Linear Algebra Concept Map",
        "graph": """
flowchart LR
    A[Vectors] --> B[Span and subspaces]
    B --> C[Linear independence]
    C --> D[Matrices and linear maps]
    D --> E[Rank and nullity]
    D --> F[Eigenvalues and eigenvectors]
    D --> G[Orthogonal projections]
    F --> H[Diagonalization and SVD]
    G --> I[Least squares and PCA]
    H --> I
""",
        "reference": "Visual intuition reference: [Essence of Linear Algebra](https://youtube.com/playlist?list=PL0-GT3co4r2y2YErbmuJw2L5tW4Ew2O5B) by 3Blue1Brown.",
    },
    "Calculus-and-Optimization-Readme.md": {
        "title": "Calculus and Optimization Concept Map",
        "graph": """
flowchart LR
    A[Functions] --> B[Limits]
    B --> C[Continuity]
    C --> D[Derivatives]
    D --> E[Taylor approximation]
    D --> F[Critical points]
    F --> G[Maxima and minima]
    G --> H[Single-variable optimization]
""",
        "reference": "Visual-first reference: [3Blue1Brown calculus topics](https://www.3blue1brown.com/topics/calculus).",
    },
    "Programming-and-Algorithms-Readme.md": {
        "title": "Programming and Algorithms Concept Map",
        "graph": """
flowchart LR
    A[Python semantics] --> B[Data structures]
    B --> C[Stacks, queues, and lists]
    B --> D[Trees and hash tables]
    C --> E[Searching and sorting]
    D --> F[Graph traversal]
    E --> G[Divide and conquer]
    F --> H[Shortest paths]
    G --> I[Complexity analysis]
    H --> I
""",
        "reference": "Diagram style follows a visual-first progression inspired by [3Blue1Brown](https://www.3blue1brown.com/).",
    },
    "Database-Management-Readme.md": {
        "title": "Database Management Concept Map",
        "graph": """
flowchart LR
    A[ER model] --> B[Relational model]
    B --> C[Relational algebra and tuple calculus]
    C --> D[SQL and integrity constraints]
    D --> E[Functional dependencies]
    E --> F[Normalization]
    D --> G[File organization and indexing]
    G --> H[Data transformations]
    H --> I[Warehousing and OLAP]
""",
        "reference": "Diagram style follows a visual-first progression inspired by [3Blue1Brown](https://www.3blue1brown.com/).",
    },
    "Machine-Learning-Readme.md": {
        "title": "Machine Learning Concept Map",
        "graph": """
flowchart LR
    A[Data and features] --> B{Learning task}
    B -->|Supervised| C[Regression]
    B -->|Supervised| D[Classification]
    B -->|Unsupervised| E[Clustering]
    B -->|Unsupervised| F[Dimensionality reduction]
    C --> G[Loss and regularization]
    D --> G
    G --> H[Bias-variance and validation]
    E --> I[k-means and hierarchical methods]
    F --> J[PCA]
""",
        "reference": "Diagram style follows a visual-first progression inspired by [3Blue1Brown](https://www.3blue1brown.com/).",
    },
    "Artificial-Intelligence-Readme.md": {
        "title": "Artificial Intelligence Concept Map",
        "graph": """
flowchart LR
    A[Agents and states] --> B{Reasoning mode}
    B --> C[Uninformed search]
    B --> D[Informed search]
    B --> E[Adversarial search]
    B --> F[Logic]
    B --> G[Reasoning under uncertainty]
    F --> H[Propositional and predicate logic]
    G --> I[Conditional independence]
    I --> J[Variable elimination]
    I --> K[Sampling]
""",
        "reference": "Diagram style follows a visual-first progression inspired by [3Blue1Brown](https://www.3blue1brown.com/).",
    },
}


def diagram_block(config):
    graph = config["graph"].strip()
    return f"""{START}
## Interactive Concept Map

Open the Mermaid diagram viewer on GitHub to pan and zoom through this original
subject map.

```mermaid
{graph}
    classDef default fill:#172033,stroke:#58c4dd,color:#ffffff,stroke-width:2px
    linkStyle default stroke:#f2cc8f,stroke-width:2px
```

{config["reference"]}
{END}"""


def updated_content(path, config):
    content = path.read_text(encoding="utf-8")
    block = diagram_block(config)
    if START in content and END in content:
        before, remainder = content.split(START, 1)
        _, after = remainder.split(END, 1)
        return before.rstrip() + "\n\n" + block + after

    separator = "\n\n---\n"
    if separator not in content:
        raise ValueError(f"Cannot find insertion point in {path}")
    before, after = content.split(separator, 1)
    return before.rstrip() + "\n\n" + block + separator + after


def main():
    parser = ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []

    for filename, config in SUBJECTS.items():
        path = ROOT / filename
        expected = updated_content(path, config)
        current = path.read_text(encoding="utf-8")
        if current == expected:
            continue
        if args.check:
            stale.append(filename)
        else:
            path.write_text(expected, encoding="utf-8")
            print(f"Updated {filename}")

    if stale:
        details = "\n".join(f"- {filename}" for filename in stale)
        raise SystemExit(
            "Generated subject diagrams are stale. Run "
            "`python scripts/generate_subject_diagrams.py`:\n" + details
        )


if __name__ == "__main__":
    main()
