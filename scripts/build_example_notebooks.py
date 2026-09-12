"""Build the repository's small, deterministic example notebooks."""

import json
from pathlib import Path
from textwrap import dedent

try:
    import nbformat as nbf
    HAS_NBF = True
except ImportError:
    HAS_NBF = False


ROOT = Path(__file__).resolve().parents[1]


def markdown(text):
    clean = dedent(text).strip()
    if HAS_NBF:
        return nbf.v4.new_markdown_cell(clean)
    lines = [line + "\n" for line in clean.splitlines()]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": lines,
    }


def code(text):
    clean = dedent(text).strip()
    if HAS_NBF:
        return nbf.v4.new_code_cell(clean)
    lines = [line + "\n" for line in clean.splitlines()]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines,
    }


def write_notebook(relative_path, cells):
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if HAS_NBF:
        notebook = nbf.v4.new_notebook(
            cells=cells,
            metadata={
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {"name": "python", "version": "3"},
            },
        )
        nbf.write(notebook, path)
    else:
        notebook = {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {"name": "python", "version": "3"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(notebook, f, indent=1)
    print(f"Wrote notebook: {relative_path}")


def build_all():
    write_notebook(
        "notebooks/probability/conditional_probability_and_bayes.ipynb",
        [
            markdown(
                """
                # Conditional Probability and Bayes Theorem

                **Syllabus mapping:** marginal, conditional, and joint probability;
                Bayes theorem.

                **Objectives:** compute a posterior probability from prevalence,
                sensitivity, and false-positive rate; distinguish
                `P(positive | disease)` from `P(disease | positive)`.
                """
            ),
            markdown(
                """
                For disease event $D$ and positive-test event $+$:

                $$P(D|+) = \\frac{P(+|D)P(D)}
                {P(+|D)P(D) + P(+|D^c)P(D^c)}.$$
                """
            ),
            code(
                """
                prevalence = 0.02
                sensitivity = 0.95
                false_positive_rate = 0.08

                p_positive = (
                    sensitivity * prevalence
                    + false_positive_rate * (1 - prevalence)
                )
                posterior = sensitivity * prevalence / p_positive

                print(f"P(positive) = {p_positive:.4f}")
                print(f"P(disease | positive) = {posterior:.4f}")
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **NAT:** A disease has prevalence `0.10`. A test has sensitivity
                `0.80` and false-positive rate `0.10`. Find
                $P(D|+)$, rounded to two decimal places.

                **MCQ:** If $A$ and $B$ are independent and both have non-zero
                probability, which is true?

                A. $P(A|B)=P(B)$
                B. $P(A|B)=P(A)$
                C. $P(A \\cap B)=P(A)+P(B)$
                D. $P(A|B)=1$
                """
            ),
            markdown(
                """
                ## Solutions

                NAT: $(0.80\\times0.10)/(0.80\\times0.10+0.10\\times0.90)
                = 0.47$.

                MCQ: **B**. Independence means observing $B$ does not change the
                probability of $A$.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/linear_algebra/projections_and_pca.ipynb",
        [
            markdown(
                """
                # Projection Matrices and PCA

                **Syllabus mapping:** projection matrix, orthogonal matrix,
                idempotent matrix, eigenvalues/eigenvectors, PCA.

                **Objectives:** construct a projection matrix, verify its defining
                properties, and connect PCA directions to covariance eigenvectors.
                """
            ),
            markdown(
                """
                For a non-zero vector $u$, the orthogonal projection onto its span
                is $P = uu^T/(u^Tu)$. An orthogonal projection is symmetric and
                idempotent: $P^T=P$ and $P^2=P$.
                """
            ),
            code(
                """
                import numpy as np

                u = np.array([1.0, 2.0])
                projection = np.outer(u, u) / (u @ u)
                x = np.array([3.0, 1.0])

                print("P =\\n", projection)
                print("Px =", projection @ x)
                print("symmetric:", np.allclose(projection.T, projection))
                print("idempotent:", np.allclose(projection @ projection, projection))
                """
            ),
            code(
                """
                samples = np.array([[2.0, 1.0], [3.0, 2.0], [4.0, 3.0], [5.0, 4.0]])
                centered = samples - samples.mean(axis=0)
                covariance = centered.T @ centered / len(samples)
                eigenvalues, eigenvectors = np.linalg.eigh(covariance)
                first_pc = eigenvectors[:, np.argmax(eigenvalues)]

                print("eigenvalues:", eigenvalues)
                print("first principal component:", first_pc)
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **MSQ:** For an orthogonal projection matrix $P$, which are always
                true?

                A. $P^T=P$
                B. $P^2=P$
                C. Every eigenvalue is either 0 or 1
                D. $P^{-1}=P$

                ## Solution

                **A, B, C.** A projection may be singular, so it need not have an
                inverse.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/algorithms/binary_search_and_complexity.ipynb",
        [
            markdown(
                """
                # Binary Search and Logarithmic Complexity

                **Syllabus mapping:** Python programming, binary search, and
                algorithm complexity.

                **Objectives:** trace binary search, count comparisons, and connect
                repeated halving to logarithmic running time.
                """
            ),
            code(
                """
                def binary_search(values, target):
                    low, high = 0, len(values) - 1
                    comparisons = 0

                    while low <= high:
                        comparisons += 1
                        middle = (low + high) // 2
                        if values[middle] == target:
                            return middle, comparisons
                        if values[middle] < target:
                            low = middle + 1
                        else:
                            high = middle - 1

                    return -1, comparisons


                values = list(range(0, 32, 2))
                for target in (18, 19):
                    print(target, binary_search(values, target))
                """
            ),
            markdown(
                """
                Each comparison discards about half of the remaining search
                interval, giving the recurrence $T(n)=T(n/2)+O(1)$ and therefore
                $T(n)=O(\\log n)$.
                """
            ),
            code(
                """
                for size in (8, 16, 32, 64, 128, 256, 512, 1024):
                    _, comparisons = binary_search(list(range(size)), -1)
                    print(f"n={size:4d}, unsuccessful-search comparisons={comparisons}")
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **MCQ:** Which recurrence describes standard binary search?

                A. $T(n)=2T(n/2)+O(1)$
                B. $T(n)=T(n-1)+O(1)$
                C. $T(n)=T(n/2)+O(1)$
                D. $T(n)=T(n/2)+O(n)$

                **NAT:** What is the maximum number of comparisons made by an
                unsuccessful binary search over 1,000 sorted distinct values?

                ## Solutions

                MCQ: **C**. NAT: **10**, because $2^9 < 1000 < 2^{10}$.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/machine_learning/linear_regression_from_scratch.ipynb",
        [
            markdown(
                """
                # Linear Regression from Scratch

                **Syllabus mapping:** simple and multiple linear regression,
                optimization involving a single variable.

                **Collaborator input:** the concept progression is informed by
                [Swakath's PRML regression assignment](https://github.com/swakath/PRML/tree/main/Regression).
                This notebook uses original code and synthetic data.

                **Objectives:** fit a line with the normal equation and understand
                a gradient-descent update.
                """
            ),
            code(
                """
                import numpy as np

                x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
                y = np.array([1.0, 3.0, 5.0, 7.0, 9.0])

                design = np.column_stack([np.ones_like(x), x])
                weights = np.linalg.solve(design.T @ design, design.T @ y)
                print("intercept, slope:", weights)
                """
            ),
            markdown(
                """
                The least-squares solution satisfies the normal equation
                $X^TXw=X^Ty$. Gradient descent instead repeatedly applies
                $w \\leftarrow w-\\eta\\nabla L(w)$.
                """
            ),
            code(
                """
                w = np.zeros(2)
                learning_rate = 0.05

                for _ in range(200):
                    residuals = design @ w - y
                    gradient = 2 * design.T @ residuals / len(y)
                    w -= learning_rate * gradient

                print("gradient-descent weights:", np.round(w, 4))
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **MCQ:** Adding an $L_2$ penalty to least squares gives:

                A. Logistic regression
                B. Ridge regression
                C. k-nearest neighbours
                D. Linear discriminant analysis

                **NAT:** For predictions `[2, 5]` and true values `[3, 3]`, what is
                the mean squared error?

                ## Solutions

                MCQ: **B**. NAT: $(1^2+2^2)/2=2.5$.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/machine_learning/logistic_classification.ipynb",
        [
            markdown(
                """
                # Logistic Classification

                **Syllabus mapping:** classification problems and logistic
                regression.

                **Collaborator input:** the concept progression is informed by
                [Swakath's PRML classification assignment](https://github.com/swakath/PRML/tree/main/Classification).
                This notebook uses original code and synthetic data.

                **Objectives:** compute sigmoid probabilities, apply a decision
                threshold, and evaluate logistic loss.
                """
            ),
            code(
                """
                import numpy as np


                def sigmoid(z):
                    return 1 / (1 + np.exp(-z))


                x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
                weight, bias = 1.5, -0.25
                probabilities = sigmoid(weight * x + bias)
                predictions = (probabilities >= 0.5).astype(int)

                print("probabilities:", np.round(probabilities, 3))
                print("predictions:", predictions)
                """
            ),
            code(
                """
                labels = np.array([0, 0, 0, 1, 1])
                epsilon = 1e-12
                loss = -np.mean(
                    labels * np.log(probabilities + epsilon)
                    + (1 - labels) * np.log(1 - probabilities + epsilon)
                )
                print(f"binary cross-entropy = {loss:.4f}")
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **MSQ:** Which statements are true for binary logistic regression?

                A. The sigmoid output lies between 0 and 1.
                B. A linear score is transformed into a probability.
                C. The default decision boundary at probability 0.5 has score 0.
                D. Logistic regression can only output labels, not probabilities.

                ## Solution

                **A, B, C.**
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/machine_learning/kmeans_from_scratch.ipynb",
        [
            markdown(
                """
                # K-Means from Scratch

                **Syllabus mapping:** clustering algorithms and k-means.

                **Collaborator input:** the concept progression is informed by
                [Swakath's PRML clustering assignment](https://github.com/swakath/PRML/tree/main/Clustering).
                This notebook uses original code and synthetic data.

                **Objectives:** perform assignment and centroid-update steps and
                understand the k-means objective.
                """
            ),
            code(
                """
                import numpy as np

                points = np.array(
                    [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0],
                     [5.0, 5.0], [5.0, 6.0], [6.0, 5.0]]
                )
                centroids = np.array([[0.0, 0.0], [6.0, 6.0]])

                for iteration in range(4):
                    squared_distances = ((points[:, None] - centroids[None, :]) ** 2).sum(axis=2)
                    labels = squared_distances.argmin(axis=1)
                    centroids = np.array([points[labels == k].mean(axis=0) for k in range(2)])
                    objective = ((points - centroids[labels]) ** 2).sum()
                    print(iteration, labels, np.round(centroids, 3), round(objective, 3))
                """
            ),
            markdown(
                """
                K-means alternates between assigning each point to its nearest
                centroid and replacing each centroid by the mean of its assigned
                points. Each step does not increase the within-cluster sum of
                squared distances.

                ## GATE-Style Practice

                **MCQ:** Which update minimizes the sum of squared Euclidean
                distances within one fixed cluster?

                A. Coordinate-wise median
                B. Arithmetic mean
                C. Farthest point
                D. Origin

                **MSQ:** Standard k-means can be sensitive to:

                A. Initial centroids
                B. Feature scaling
                C. Outliers
                D. The ordering of class labels

                ## Solutions

                MCQ: **B**. MSQ: **A, B, C**.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/calculus/single_variable_optimization.ipynb",
        [
            markdown(
                """
                # Single-Variable Optimization and Taylor Series

                **Syllabus mapping:** functions of a single variable, limit,
                continuity and differentiability, Taylor series, maxima and minima,
                optimization involving a single variable.

                **Objectives:** analyze critical points, classify local extrema with
                first and second derivatives, construct Taylor polynomial
                approximations, and solve 1D constrained optimization problems.
                """
            ),
            markdown(
                """
                For a differentiable function $f(x)$, critical points satisfy
                $f'(x) = 0$. By the second derivative test:
                - $f''(x^*) > 0 \\implies$ local minimum
                - $f''(x^*) < 0 \\implies$ local maximum
                - $f''(x^*) = 0 \\implies$ inconclusive (test higher-order derivatives)

                The $n$-th order Taylor polynomial of $f(x)$ around $x_0$ is:
                $$P_n(x) = \\sum_{k=0}^n \\frac{f^{(k)}(x_0)}{k!}(x - x_0)^k.$$
                """
            ),
            code(
                """
                import numpy as np

                # Analyze f(x) = 2x^3 - 3x^2 - 12x + 5 on interval [-2, 3]
                # f'(x) = 6x^2 - 6x - 12 = 6(x - 2)(x + 1)
                # Critical points: x = -1, x = 2

                def f(x):
                    return 2 * x**3 - 3 * x**2 - 12 * x + 5

                def f_prime(x):
                    return 6 * x**2 - 6 * x - 12

                def f_double_prime(x):
                    return 12 * x - 6

                critical_points = [-1.0, 2.0]
                for cp in critical_points:
                    val = f(cp)
                    d2 = f_double_prime(cp)
                    classification = "Local Maximum" if d2 < 0 else "Local Minimum"
                    print(f"Critical point x = {cp:4.1f}: f(x) = {val:6.1f}, f''(x) = {d2:5.1f} -> {classification}")

                # Check boundary points for global extrema on [-2, 3]
                interval = [-2.0, -1.0, 2.0, 3.0]
                values = {x: f(x) for x in interval}
                print("\\nValues at critical and boundary points:", values)
                print(f"Global Maximum on [-2, 3]: {max(values.values())} at x = {max(values, key=values.get)}")
                print(f"Global Minimum on [-2, 3]: {min(values.values())} at x = {min(values, key=values.get)}")
                """
            ),
            code(
                """
                # Taylor polynomial approximation of exp(x) around x0 = 0
                import math

                def taylor_exp(x, order):
                    return sum((x**k) / math.factorial(k) for k in range(order + 1))

                x_test = 0.5
                true_val = math.exp(x_test)
                print(f"True exp({x_test}) = {true_val:.8f}")
                for order in (1, 2, 3, 4):
                    approx = taylor_exp(x_test, order)
                    abs_error = abs(true_val - approx)
                    print(f"Order {order}: approx = {approx:.8f}, error = {abs_error:.8e}")
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **MCQ:** For the function $f(x) = x^3 - 3x^2 + 3x + 7$, what is the
                nature of the point $x = 1$?

                A. Local minimum
                B. Local maximum
                C. Point of inflection (stationary inflection point)
                D. Discontinuity

                **MSQ:** Which of the following statements are true for a twice
                continuously differentiable function $f: \\mathbb{R} \\to \\mathbb{R}$?

                A. If $f'(c) = 0$ and $f''(c) > 0$, then $c$ is a local minimum.
                B. If $c$ is an unconstrained local extremum in an open interval, then $f'(c) = 0$.
                C. If $f''(x) \\ge 0$ for all $x \\in \\mathbb{R}$, then $f$ is convex and every critical point is a global minimum.
                D. If $f''(c) = 0$, then $c$ must be a local extremum.

                **NAT:** What is the maximum value of $f(x) = -x^2 + 6x - 4$ on the
                closed interval $[0, 5]$?
                """
            ),
            markdown(
                """
                ## Solutions

                MCQ: **C**. $f'(x) = 3x^2 - 6x + 3 = 3(x-1)^2$. At $x=1$, $f'(1) = 0$ and
                $f''(1) = 6(1)-6 = 0$, while $f'''(1) = 6 \\ne 0$. Furthermore,
                $f'(x) \\ge 0$ for all $x$, so the function is monotonically increasing and
                $x=1$ is an inflection point.

                MSQ: **A, B, C**. (D is false: $f(x) = x^3$ has $f''(0) = 0$ but $x=0$ is an
                inflection point, not an extremum).

                NAT: **5.0**. $f'(x) = -2x + 6 = 0 \\implies x = 3 \\in [0, 5]$. Since
                $f''(x) = -2 < 0$, $x=3$ is a local maximum with value
                $f(3) = -(9) + 18 - 4 = 5$. At the boundaries: $f(0) = -4$ and
                $f(5) = -25 + 30 - 4 = 1$. The maximum value on $[0, 5]$ is **5**.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/databases/relational_algebra_and_sql.ipynb",
        [
            markdown(
                """
                # Relational Algebra, SQL, and Integrity Constraints

                **Syllabus mapping:** ER-model, relational model: relational algebra,
                tuple calculus, SQL, integrity constraints, normal form.

                **Objectives:** verify relational algebra operations (selection,
                projection, natural join, set difference), translate relational
                algebra to SQL, enforce integrity constraints, and test functional
                dependencies.
                """
            ),
            code(
                """
                import sqlite3

                conn = sqlite3.connect(":memory:")
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                # Schema with Primary Key and Foreign Key constraints
                cursor.execute(
                    \"\"\"
                    CREATE TABLE Students (
                        sid INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        department TEXT NOT NULL
                    );
                    \"\"\"
                )

                cursor.execute(
                    \"\"\"
                    CREATE TABLE Enrollments (
                        sid INTEGER,
                        course_id TEXT,
                        grade TEXT CHECK (grade IN ('A', 'B', 'C', 'F')),
                        PRIMARY KEY (sid, course_id),
                        FOREIGN KEY (sid) REFERENCES Students(sid) ON DELETE CASCADE
                    );
                    \"\"\"
                )

                cursor.executemany(
                    "INSERT INTO Students VALUES (?, ?, ?);",
                    [
                        (1, "Aarav", "CSE"),
                        (2, "Diya", "AI"),
                        (3, "Ishaan", "ECE"),
                        (4, "Meera", "CSE"),
                    ],
                )

                cursor.executemany(
                    "INSERT INTO Enrollments VALUES (?, ?, ?);",
                    [
                        (1, "CS101", "A"),
                        (1, "MA101", "B"),
                        (2, "CS101", "A"),
                        (2, "AI201", "A"),
                        (3, "CS101", "B"),
                    ],
                )
                conn.commit()
                print("Database populated successfully.")
                """
            ),
            code(
                """
                # Relational Algebra 1: Selection (sigma_{department='CSE'}(Students))
                print("--- Selection sigma_{department='CSE'} ---")
                cursor.execute("SELECT * FROM Students WHERE department = 'CSE';")
                print(cursor.fetchall())

                # Relational Algebra 2: Projection (pi_{name}(Students))
                print("\\n--- Projection pi_{name} ---")
                cursor.execute("SELECT name FROM Students;")
                print(cursor.fetchall())

                # Relational Algebra 3: Natural Join (Students bowtie Enrollments)
                print("\\n--- Natural Join (Students JOIN Enrollments) ---")
                cursor.execute(
                    \"\"\"
                    SELECT Students.sid, Students.name, Enrollments.course_id, Enrollments.grade
                    FROM Students
                    INNER JOIN Enrollments ON Students.sid = Enrollments.sid;
                    \"\"\"
                )
                for row in cursor.fetchall():
                    print(row)

                # Relational Algebra 4: Set Difference (pi_{sid}(Students) - pi_{sid}(Enrollments))
                print("\\n--- Students not enrolled in any course (Set Difference) ---")
                cursor.execute(
                    \"\"\"
                    SELECT sid, name FROM Students
                    WHERE sid NOT IN (SELECT sid FROM Enrollments);
                    \"\"\"
                )
                print(cursor.fetchall())
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **MCQ:** In relational algebra, which algebraic expression represents
                the relational division $R(A, B) \\div S(B)$ (finding all $A$ values
                associated with *every* $B$ value in $S$)?

                A. $\\pi_A(R) - \\pi_A((\\pi_A(R) \\times S) - R)$
                B. $\\pi_A(R) \\cap \\pi_B(S)$
                C. $\\pi_A(R \\bowtie S)$
                D. $\\pi_A(R) \\cup S$

                **MSQ:** Which of the following statements regarding database normalization
                are true?

                A. Every relational schema in BCNF is also in 3NF.
                B. Any relational schema can be decomposed into a set of 3NF relations such that the decomposition is both lossless-join and dependency-preserving.
                C. Any relational schema can always be decomposed into BCNF relations such that the decomposition is both lossless-join and dependency-preserving.
                D. In BCNF, for every non-trivial functional dependency $X \\to Y$, $X$ must be a superkey.

                **NAT:** Given relation $R(A, B)$ with 6 tuples and relation $S(B, C)$
                with 5 tuples. What is the **maximum possible** number of tuples in
                the natural join $R \\bowtie S$?
                """
            ),
            markdown(
                """
                ## Solutions

                MCQ: **A**. By definition, relational division $R \\div S$ produces the
                tuples in $\\pi_A(R)$ that do NOT fail to match some tuple in $S$. The
                term $(\\pi_A(R) \\times S) - R$ gives all pairs $(a, b)$ missing from $R$;
                projecting on $A$ and subtracting from $\\pi_A(R)$ gives those $A$ values
                present with all $B \\in S$.

                MSQ: **A, B, D**. (C is false: while a lossless-join BCNF decomposition
                is always achievable, functional dependencies may not always be preserved
                in BCNF).

                NAT: **30**. If all 6 tuples of $R$ and all 5 tuples of $S$ share the
                identical value for the join attribute $B$, every tuple of $R$ pairs with
                every tuple of $S$, yielding $6 \\times 5 = 30$ tuples.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/ai/search_and_uncertainty.ipynb",
        [
            markdown(
                """
                # AI Search and Reasoning Under Uncertainty

                **Syllabus mapping:** Search: informed, uninformed, adversarial;
                logic: propositional, predicate; reasoning under uncertainty topics:
                conditional independence representation, exact inference through
                variable elimination, approximate inference through sampling.

                **Objectives:** trace A* search with admissible heuristics, implement
                adversarial Minimax evaluation, and perform exact inference via
                Variable Elimination on a Bayesian Network.
                """
            ),
            code(
                """
                import heapq

                # 1. Informed Search: A* on a weighted directed graph
                # f(n) = g(n) + h(n)

                graph = {
                    "S": [("A", 2), ("B", 4)],
                    "A": [("C", 3), ("D", 4)],
                    "B": [("D", 1)],
                    "C": [("G", 4)],
                    "D": [("G", 2)],
                    "G": [],
                }

                heuristic = {"S": 5, "A": 4, "B": 2, "C": 3, "D": 2, "G": 0}


                def a_star(graph, start, goal, h):
                    pq = [(h[start], 0, start, [start])]
                    visited = set()

                    while pq:
                        f, g, current, path = heapq.heappop(pq)
                        print(f"Expanding {current}: g={g}, h={h[current]}, f={f}")
                        if current == goal:
                            return path, g
                        if current in visited:
                            continue
                        visited.add(current)

                        for neighbor, cost in graph.get(current, []):
                            if neighbor not in visited:
                                next_g = g + cost
                                next_f = next_g + h[neighbor]
                                heapq.heappush(pq, (next_f, next_g, neighbor, path + [neighbor]))

                    return None, float("inf")


                path, total_cost = a_star(graph, "S", "G", heuristic)
                print(f"\\nA* Optimal Path: {' -> '.join(path)}, Total Cost: {total_cost}")
                """
            ),
            code(
                """
                # 2. Reasoning Under Uncertainty: Variable Elimination on A -> B -> C
                # P(A=1) = 0.2
                # P(B=1|A=1) = 0.8, P(B=1|A=0) = 0.3
                # P(C=1|B=1) = 0.9, P(C=1|B=0) = 0.1
                # Find P(C=1 | A=1) by eliminating B:
                # P(C=1 | A=1) = sum_b P(C=1|b) * P(b|A=1)

                p_a = {1: 0.2, 0: 0.8}
                p_b_given_a = {(1, 1): 0.8, (0, 1): 0.2, (1, 0): 0.3, (0, 0): 0.7}
                p_c_given_b = {(1, 1): 0.9, (0, 1): 0.1, (1, 0): 0.1, (0, 0): 0.9}

                # Variable elimination for P(C=1 | A=1)
                p_c1_given_a1 = sum(
                    p_c_given_b[(1, b)] * p_b_given_a[(b, 1)] for b in (0, 1)
                )
                print(f"Exact Inference P(C=1 | A=1) = {p_c1_given_a1:.4f}")

                # 3. Approximate Inference: Rejection Sampling
                import random
                random.seed(42)
                N = 100000
                accepted_c1 = 0
                total_accepted = 0

                for _ in range(N):
                    # Sample A
                    a = 1 if random.random() < p_a[1] else 0
                    if a != 1:  # Reject sample because evidence is A=1
                        continue
                    total_accepted += 1
                    # Sample B given A=1
                    b = 1 if random.random() < p_b_given_a[(1, 1)] else 0
                    # Sample C given B
                    c = 1 if random.random() < p_c_given_b[(1, b)] else 0
                    if c == 1:
                        accepted_c1 += 1

                sampled_prob = accepted_c1 / total_accepted
                print(f"Sampled Estimate P(C=1 | A=1) = {sampled_prob:.4f} (from {total_accepted} samples)")
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **MCQ:** In A* graph search, which property of the heuristic function
                $h(n)$ guarantees that the first time a goal node is expanded, an
                optimal path has been found, even when nodes are not reopened?

                A. Admissibility ($h(n) \\le h^*(n)$)
                B. Consistency / Monotonicity ($h(n) \\le c(n, a, n') + h(n')$)
                C. Dominance ($h(n) > h'(n)$)
                D. Boundedness ($h(n) \\ge 0$)

                **MSQ:** In a Bayesian Network with causal chain structure $X \\to Y \\to Z$,
                which of the following conditional independence statements are true?

                A. $X$ and $Z$ are conditionally independent given $Y$ ($X \\perp Z \\mid Y$).
                B. $X$ and $Z$ are marginally independent ($X \\perp Z$).
                C. $P(Z \\mid Y, X) = P(Z \\mid Y)$.
                D. Observing $Y$ blocks the active path between $X$ and $Z$.

                **NAT:** Consider a two-player zero-sum game tree where the root is a
                MAX node with two actions $L$ and $R$. The subtree under $L$ has two
                leaves with payoff values 4 and 7. The subtree under $R$ has two leaves
                with payoff values 2 and 9. What is the minimax value at the root node?
                """
            ),
            markdown(
                """
                ## Solutions

                MCQ: **B**. In graph search without node reopening, consistency
                (monotonicity) is required to guarantee optimality. (Admissibility alone
                suffices for tree search or when closed nodes can be reopened).

                MSQ: **A, C, D**. In a causal chain $X \\to Y \\to Z$, conditioning on $Y$
                d-separates $X$ and $Z$, making them conditionally independent. (B is
                false: knowing $X$ alters the probability of $Y$, which in turn alters $Z$;
                they are marginally dependent).

                NAT: **4.0**. The children of the root are MIN nodes. Under action $L$,
                the MIN player chooses $\\min(4, 7) = 4$. Under action $R$, the MIN player
                chooses $\\min(2, 9) = 2$. At the root, the MAX player chooses
                $\\max(4, 2) = 4$.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/machine_learning/hierarchical_clustering.ipynb",
        [
            markdown(
                """
                # Hierarchical Clustering (Top-down, Bottom-up, Single and Multiple Linkage)

                **Syllabus mapping:** Unsupervised Learning: clustering algorithms,
                k-means/k-medoid, hierarchical clustering, top-down, bottom-up:
                single-linkage, multiple-linkage, dimensionality reduction,
                principal component analysis.

                **Objectives:** compute pairwise distance matrices, implement bottom-up
                (agglomerative) hierarchical clustering, contrast Single-Linkage
                (minimum distance) with Complete-Linkage (maximum distance), and
                understand the chaining effect.
                """
            ),
            markdown(
                """
                Given two clusters $C_i$ and $C_j$:
                - **Single-Linkage:** $D(C_i, C_j) = \\min_{x \\in C_i, y \\in C_j} d(x, y)$
                - **Complete-Linkage (Multiple-Linkage):** $D(C_i, C_j) = \\max_{x \\in C_i, y \\in C_j} d(x, y)$
                - **Average-Linkage:** $D(C_i, C_j) = \\frac{1}{|C_i||C_j|} \\sum_{x \\in C_i, y \\in C_j} d(x, y)$
                """
            ),
            code(
                """
                import numpy as np

                # 5 data points in 2D
                points = np.array([
                    [1.0, 1.0],   # P0
                    [1.5, 1.5],   # P1
                    [5.0, 5.0],   # P2
                    [5.5, 5.0],   # P3
                    [3.0, 3.0],   # P4
                ])
                labels = ["P0", "P1", "P2", "P3", "P4"]

                # Compute pairwise Euclidean distance matrix
                diffs = points[:, None, :] - points[None, :, :]
                distance_matrix = np.sqrt((diffs**2).sum(axis=-1))

                print("Pairwise Distance Matrix:")
                print("     " + " ".join(f"{l:>6}" for l in labels))
                for i, row in enumerate(distance_matrix):
                    print(f"{labels[i]:>3}: " + " ".join(f"{v:6.3f}" for v in row))
                """
            ),
            code(
                """
                # Agglomerative clustering step-by-step with Single Linkage
                clusters = {i: [labels[i]] for i in range(len(points))}
                dist_mat = distance_matrix.copy()
                np.fill_diagonal(dist_mat, np.inf)

                print("\\n--- Single-Linkage Merge Sequence ---")
                step = 1
                while len(clusters) > 1:
                    i, j = np.unravel_index(dist_mat.argmin(), dist_mat.shape)
                    min_dist = dist_mat[i, j]
                    print(f"Step {step}: Merge {clusters[i]} and {clusters[j]} at distance {min_dist:.3f}")

                    # Merge j into i
                    clusters[i] = clusters[i] + clusters[j]
                    del clusters[j]

                    # Update single linkage: min distance to newly formed cluster
                    for k in clusters:
                        if k != i:
                            new_d = min(dist_mat[i, k], dist_mat[j, k])
                            dist_mat[i, k] = dist_mat[k, i] = new_d

                    dist_mat[j, :] = dist_mat[:, j] = np.inf
                    step += 1
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **MCQ:** In agglomerative hierarchical clustering, the **chaining effect**
                (forming extended, straggly clusters connected by a series of intermediate
                points) is a well-known limitation of:

                A. Complete-linkage
                B. Single-linkage
                C. Average-linkage
                D. Centroid method

                **MSQ:** Which of the following statements about hierarchical clustering
                are true?

                A. Agglomerative clustering is bottom-up; divisive clustering is top-down.
                B. Complete-linkage uses the maximum distance between points in two clusters.
                C. Single-linkage is less sensitive to noise and outliers than complete-linkage.
                D. Unlike k-means, hierarchical agglomerative clustering is deterministic and does not require random initialization.

                **NAT:** Consider 4 one-dimensional data points: $x_1 = 1.0, x_2 = 4.0, x_3 = 8.0, x_4 = 10.0$.
                In agglomerative hierarchical clustering using **single-linkage** with
                Euclidean distance, at what distance does the **second** cluster merge occur?
                """
            ),
            markdown(
                """
                ## Solutions

                MCQ: **B**. Single-linkage merges clusters based on the minimum pairwise
                distance ($D(A, B) = \\min_{x \\in A, y \\in B} d(x, y)$), which can create
                long chains of nearby points.

                MSQ: **A, B, D**. (C is false: single-linkage is highly vulnerable to noise
                points bridging distinct clusters, causing premature chaining).

                NAT: **3.0**.
                - Pairwise distances: $|x_1-x_2|=3$, $|x_2-x_3|=4$, $|x_3-x_4|=2$.
                - First merge: $\\{x_3\\}$ and $\\{x_4\\}$ at distance $2.0$.
                - Remaining clusters: $\\{x_1\\}$, $\\{x_2\\}$, $\\{x_3, x_4\\}$.
                - Cluster distances:
                  - $d(\\{x_1\\}, \\{x_2\\}) = 3.0$
                  - $d(\\{x_2\\}, \\{x_3, x_4\\}) = \\min(4, 6) = 4.0$
                  - $d(\\{x_1\\}, \\{x_3, x_4\\}) = \\min(7, 9) = 7.0$
                - The minimum distance among remaining clusters is $3.0$ between
                  $\\{x_1\\}$ and $\\{x_2\\}$. Thus, the second merge occurs at distance **3.0**.
                """
            ),
        ],
    )


if __name__ == "__main__":
    build_all()
