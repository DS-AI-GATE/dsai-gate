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

    write_notebook(
        "notebooks/probability/statistical_inference_and_tests.ipynb",
        [
            markdown(
                """
                # Statistical Inference, Confidence Intervals, and Hypothesis Testing

                **Syllabus mapping:** Central limit theorem, confidence interval,
                z-test, t-test, chi-squared test.

                **Objectives:** compute sample statistics; construct confidence intervals
                for population mean; perform one-sample z-tests and t-tests; compute the
                chi-squared goodness-of-fit test statistic; interpret p-values and critical regions.
                """
            ),
            markdown(
                """
                ## Theoretical Foundations

                ### 1. Confidence Interval for Population Mean
                When population variance $\\sigma^2$ is known (or sample size $n$ is large via CLT):
                $$CI_{1-\\alpha} = \\bar{x} \\pm z_{\\alpha/2} \\frac{\\sigma}{\\sqrt{n}}$$

                When $\\sigma$ is unknown and sample size $n$ is small (from a normal population):
                $$CI_{1-\\alpha} = \\bar{x} \\pm t_{\\alpha/2, n-1} \\frac{s}{\\sqrt{n}}$$
                where $s = \\sqrt{\\frac{1}{n-1} \\sum_{i=1}^n (x_i - \\bar{x})^2}$ is the sample standard deviation.

                ### 2. Hypothesis Testing
                - **z-test statistic:** $z = \\frac{\\bar{x} - \\mu_0}{\\sigma / \\sqrt{n}}$
                - **t-test statistic:** $t = \\frac{\\bar{x} - \\mu_0}{s / \\sqrt{n}}$ with $df = n - 1$
                - **Chi-squared test for goodness of fit:**
                  $$\\chi^2 = \\sum_{i=1}^k \\frac{(O_i - E_i)^2}{E_i}$$
                  where $O_i$ is observed frequency, $E_i$ is expected frequency, with degrees of freedom $df = k - 1 - p$.
                """
            ),
            code(
                """
                import numpy as np
                from scipy import stats

                np.random.seed(42)

                # Sample data: 36 measurements
                sample = np.array([
                    51.2, 53.1, 49.8, 54.0, 52.5, 50.9, 53.4, 52.0, 51.8, 53.6,
                    52.2, 54.1, 51.5, 50.4, 53.8, 52.9, 51.7, 53.2, 52.1, 54.5,
                    50.8, 52.6, 53.0, 51.9, 54.2, 52.3, 51.1, 53.7, 52.4, 50.6,
                    53.5, 52.8, 51.6, 54.3, 52.7, 51.4
                ])
                n = len(sample)
                x_bar = np.mean(sample)
                s = np.std(sample, ddof=1)
                se = s / np.sqrt(n)

                print(f"Sample size n = {n}")
                print(f"Sample mean x_bar = {x_bar:.2f}")
                print(f"Sample std s = {s:.2f}")
                print(f"Standard Error SE = {se:.4f}")

                # 95% Confidence Interval with t-distribution
                alpha = 0.05
                t_crit = stats.t.ppf(1 - alpha / 2, df=n - 1)
                ci_lower = x_bar - t_crit * se
                ci_upper = x_bar + t_crit * se
                print(f"95% CI (t-dist): [{ci_lower:.3f}, {ci_upper:.3f}]")

                # Hypothesis Test: H0: mu = 50 vs H1: mu != 50
                mu_0 = 50.0
                t_stat = (x_bar - mu_0) / se
                p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n - 1))
                print(f"t-statistic = {t_stat:.4f}, p-value = {p_value:.6e}")
                print("Decision at alpha=0.05:", "Reject H0" if p_value < 0.05 else "Fail to reject H0")

                # Chi-Squared Goodness of Fit Test
                # Testing if a 6-sided die is fair across 120 rolls
                observed = np.array([22, 18, 25, 15, 24, 16])
                expected = np.array([20, 20, 20, 20, 20, 20])
                chi2_stat = np.sum((observed - expected) ** 2 / expected)
                chi2_p_val = 1 - stats.chi2.cdf(chi2_stat, df=len(observed) - 1)
                print(f"\\nChi-squared statistic = {chi2_stat:.4f}, p-value = {chi2_p_val:.4f}")
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **NAT:** A random sample of $n = 36$ observations from a normal population
                with known standard deviation $\\sigma = 6$ yields a sample mean $\\bar{x} = 52.5$.
                To test the hypothesis $H_0: \\mu = 50$ against $H_1: \\mu > 50$, compute the
                value of the calculated test statistic $z$.

                **MCQ:** In hypothesis testing, which of the following defines a **Type I error**?

                A. Rejecting the null hypothesis $H_0$ when $H_0$ is true.
                B. Failing to reject $H_0$ when $H_0$ is false.
                C. Rejecting the alternative hypothesis $H_1$ when $H_1$ is true.
                D. Accepting $H_0$ when the p-value is less than the significance level $\\alpha$.

                **MSQ:** Which of the following statements regarding Student's $t$-distribution
                and the standard normal distribution are TRUE?

                A. As the degrees of freedom $df \\to \\infty$, the $t$-distribution converges to the standard normal distribution $\\mathcal{N}(0, 1)$.
                B. The $t$-distribution is symmetric about zero and bell-shaped, but has fatter (heavier) tails than the standard normal distribution.
                C. The variance of a $t$-distribution with $k > 2$ degrees of freedom is $\\frac{k}{k-2}$, which is strictly greater than 1.
                D. When population variance $\\sigma^2$ is known, a $t$-test is preferred over a $z$-test for any sample size $n$.
                """
            ),
            markdown(
                """
                ## Solutions

                NAT: **2.5**.
                $$z = \\frac{\\bar{x} - \\mu_0}{\\sigma / \\sqrt{n}} = \\frac{52.5 - 50}{6 / \\sqrt{36}} = \\frac{2.5}{6 / 6} = \\frac{2.5}{1} = 2.5.$$

                MCQ: **A**. A Type I error occurs when the null hypothesis $H_0$ is rejected
                even though it is true. The probability of committing a Type I error equals the
                significance level $\\alpha$.

                MSQ: **A, B, C**.
                - A is true: CLT and Slutsky's theorem ensure convergence to $\\mathcal{N}(0, 1)$ as $df \\to \\infty$.
                - B is true: Heavy tails reflect the added uncertainty of estimating $\\sigma$ with $s$.
                - C is true: $\\text{Var}(T) = \\frac{k}{k-2} > 1$ for $k > 2$.
                - D is false: When $\\sigma^2$ is known, the $z$-test is the exact test regardless of sample size $n$.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/linear_algebra/partition_matrices_and_lu.ipynb",
        [
            markdown(
                """
                # Partition Matrices and LU Decomposition

                **Syllabus mapping:** partition matrix and their properties,
                systems of linear equations and solutions, Gaussian elimination,
                LU decomposition.

                **Objectives:** understand block matrix multiplication, determinants
                of block triangular matrices, and Schur complements; compute LU
                decomposition $A = LU$ and solve linear systems via forward/back substitution.
                """
            ),
            markdown(
                """
                ## Theoretical Foundations

                ### 1. Partition (Block) Matrices
                For conformably partitioned matrices:
                $$\\begin{bmatrix} A & B \\\\ C & D \\end{bmatrix} \\begin{bmatrix} X \\\\ Y \\end{bmatrix} = \\begin{bmatrix} AX + BY \\\\ CX + DY \\end{bmatrix}$$

                For block triangular matrices:
                $$\\det \\begin{bmatrix} A & B \\\\ 0 & D \\end{bmatrix} = \\det(A) \\det(D)$$

                When $A$ is invertible, the block inverse is given via the Schur complement $S = D - CA^{-1}B$:
                $$\\det \\begin{bmatrix} A & B \\\\ C & D \\end{bmatrix} = \\det(A) \\det(D - CA^{-1}B)$$

                ### 2. LU Decomposition
                Gaussian elimination without row interchanges factors a matrix $A$ into $A = LU$, where:
                - $L$ is unit lower triangular ($l_{ii} = 1$, $l_{ij} = 0$ for $j > i$).
                - $U$ is upper triangular ($u_{ij} = 0$ for $i > j$).

                Solving $Ax = b$ becomes two $O(n^2)$ triangular solves:
                1. Forward substitution: $Ly = b$
                2. Back substitution: $Ux = y$
                """
            ),
            code(
                """
                import numpy as np

                # 1. Partition Matrix Determinant & Multiplication
                A = np.array([[2.0, 1.0], [1.0, 3.0]])
                B = np.array([[1.0, 0.0], [2.0, 1.0]])
                zero_block = np.zeros((2, 2))
                D = np.array([[4.0, 2.0], [1.0, 2.0]])

                # Construct 4x4 block matrix M = [[A, B], [0, D]]
                M = np.block([[A, B], [zero_block, D]])
                det_M = np.linalg.det(M)
                det_formula = np.linalg.det(A) * np.linalg.det(D)

                print("Block Matrix M:\\n", M)
                print(f"det(M) directly: {det_M:.4f}")
                print(f"det(A)*det(D):   {det_formula:.4f}")

                # 2. LU Decomposition from Scratch (Doolittle Algorithm)
                def lu_factorize(mat):
                    n = mat.shape[0]
                    L = np.eye(n)
                    U = np.zeros((n, n))
                    for i in range(n):
                        for j in range(i, n):
                            U[i, j] = mat[i, j] - sum(L[i, k] * U[k, j] for k in range(i))
                        for j in range(i + 1, n):
                            L[j, i] = (mat[j, i] - sum(L[j, k] * U[k, i] for k in range(i))) / U[i, i]
                    return L, U

                # Solve Ax = b
                A_sys = np.array([[2.0, 1.0, 1.0],
                                  [4.0, 1.0, 0.0],
                                  [-2.0, 2.0, 1.0]])
                b = np.array([4.0, 5.0, 1.0])

                L_mat, U_mat = lu_factorize(A_sys)
                print("\\n--- LU Factorization ---")
                print("L:\\n", L_mat)
                print("U:\\n", U_mat)
                print("Verification norm ||A - LU||:", np.linalg.norm(A_sys - L_mat @ U_mat))

                # Forward substitution: Ly = b
                y = np.zeros_like(b)
                for i in range(len(b)):
                    y[i] = b[i] - sum(L_mat[i, k] * y[k] for k in range(i))

                # Back substitution: Ux = y
                x = np.zeros_like(b)
                for i in range(len(b) - 1, -1, -1):
                    x[i] = (y[i] - sum(U_mat[i, k] * x[k] for k in range(i + 1, len(b)))) / U_mat[i, i]

                print(f"Solution x = {x}")
                print(f"Verification Ax = {A_sys @ x} (expected {b})")
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **NAT:** Let $M = \\begin{bmatrix} A & B \\\\ 0 & D \\end{bmatrix}$ be a $4 \\times 4$ block
                upper triangular matrix where $A = \\begin{bmatrix} 2 & 1 \\\\ 1 & 3 \\end{bmatrix}$ and
                $D = \\begin{bmatrix} 4 & 2 \\\\ 1 & 2 \\end{bmatrix}$. If $B$ is any arbitrary $2 \\times 2$ matrix,
                find the determinant $\\det(M)$.

                **MCQ:** In the Doolittle LU decomposition $A = LU$ (where $L$ has unit diagonal) of
                $A = \\begin{bmatrix} 2 & 1 \\\\ 6 & 8 \\end{bmatrix}$, what is the value of entry $u_{22}$ in $U$?

                A. 3
                B. 5
                C. 8
                D. 2

                **MSQ:** Which of the following statements regarding LU decomposition and matrix properties are TRUE?

                A. For any non-singular square matrix $A$, there exists a permutation matrix $P$ such that $PA = LU$.
                B. If all leading principal submatrices of $A$ are non-singular, then $A$ has a unique decomposition $A = LU$ where $L$ is unit lower triangular.
                C. Inverting a triangular matrix takes $O(n^3)$ operations.
                D. The determinant of $A = LU$ equals the product of the diagonal elements of $U$.
                """
            ),
            markdown(
                """
                ## Solutions

                NAT: **30**.
                For a block upper triangular matrix with zero bottom-left block:
                $$\\det(M) = \\det(A) \\det(D).$$
                $$\\det(A) = 2(3) - 1(1) = 5.$$
                $$\\det(D) = 4(2) - 2(1) = 6.$$
                $$\\det(M) = 5 \\times 6 = 30.$$

                MCQ: **B**.
                - First row of $U$: $u_{11} = a_{11} = 2$, $u_{12} = a_{12} = 1$.
                - First column of $L$: $l_{21} = a_{21} / u_{11} = 6 / 2 = 3$.
                - Second row of $U$: $u_{22} = a_{22} - l_{21} u_{12} = 8 - (3)(1) = 5$.

                MSQ: **A, B, D**.
                - A is true: Gaussian elimination with partial pivoting always yields $PA = LU$.
                - B is true: Non-zero pivots ensure no division by zero, yielding a unique Doolittle factorization.
                - C is false: Forward/back substitution for triangular matrices takes $O(n^2)$ operations.
                - D is true: $\\det(A) = \\det(L)\\det(U) = 1 \\times \\prod_{i=1}^n u_{ii}$.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/databases/normalization_and_calculus.ipynb",
        [
            markdown(
                """
                # Database Normalization, Functional Dependencies, and Relational Calculus

                **Syllabus mapping:** relational model: relational algebra, tuple calculus;
                integrity constraints; normal form.

                **Objectives:** compute attribute closures $X^+$; find all candidate keys;
                test for 2NF, 3NF, and BCNF violations; evaluate lossless join decomposition;
                formulate and understand declarative Tuple Relational Calculus (TRC) queries.
                """
            ),
            markdown(
                """
                ## Theoretical Foundations

                ### 1. Functional Dependencies and Keys
                - **Attribute Closure $(X)^+$:** The set of all attributes functionally determined by $X$ under FD set $F$.
                - **Superkey:** $K$ is a superkey if $(K)^+ = R$.
                - **Candidate Key:** A minimal superkey (no proper subset of $K$ is a superkey).
                - **Prime Attribute:** An attribute that is a member of *any* candidate key.

                ### 2. Normal Forms Hierarchy
                $$BCNF \\subset 3NF \\subset 2NF \\subset 1NF$$
                - **1NF:** All attribute domains contain only atomic (indivisible) values.
                - **2NF:** 1NF and **no partial dependency** (no non-prime attribute depends on a proper subset of any candidate key).
                - **3NF:** For every non-trivial FD $X \\to Y$:
                  - $X$ is a superkey, **OR**
                  - $Y$ is a prime attribute.
                - **BCNF:** For every non-trivial FD $X \\to Y$:
                  - $X$ **must** be a superkey.

                ### 3. Lossless Join Decomposition
                A decomposition of $R$ into $(R_1, R_2)$ is **lossless** if and only if:
                $$(R_1 \\cap R_2) \\to R_1 \\in F^+ \\quad \\text{or} \\quad (R_1 \\cap R_2) \\to R_2 \\in F^+$$

                ### 4. Tuple Relational Calculus (TRC)
                Declarative query language: $\\{t \\mid P(t)\\}$.
                - Existential quantifier: $\\exists s \\in R (P(s))$
                - Universal quantifier: $\\forall s \\in R (P(s))$
                """
            ),
            code(
                """
                from itertools import combinations

                # Attribute Closure Algorithm
                def compute_closure(attributes, fds):
                    closure = set(attributes)
                    while True:
                        updated = False
                        for lhs, rhs in fds:
                            if lhs.issubset(closure) and not rhs.issubset(closure):
                                closure.update(rhs)
                                updated = True
                        if not updated:
                            break
                    return closure

                # Candidate Keys Finder
                def find_candidate_keys(relation_attrs, fds):
                    all_attrs = set(relation_attrs)
                    candidate_keys = []
                    for r in range(1, len(all_attrs) + 1):
                        for subset in combinations(sorted(all_attrs), r):
                            s = set(subset)
                            # Minimal check: no existing CK is a subset of s
                            if any(set(ck).issubset(s) for ck in candidate_keys):
                                continue
                            if compute_closure(s, fds) == all_attrs:
                                candidate_keys.append("".join(sorted(s)))
                    return candidate_keys

                # Test Relation R(A, B, C, D, E)
                R_attrs = set("ABCDE")
                F = [
                    ({"A"}, {"B", "C"}),
                    ({"C", "D"}, {"E"}),
                    ({"B"}, {"D"}),
                    ({"E"}, {"A"}),
                ]

                keys = find_candidate_keys(R_attrs, F)
                print(f"Relation R(A, B, C, D, E)")
                print(f"Candidate Keys: {keys} (Total: {len(keys)})")

                prime_attrs = set("".join(keys))
                non_prime = R_attrs - prime_attrs
                print(f"Prime Attributes: {sorted(prime_attrs)}")
                print(f"Non-Prime Attributes: {sorted(non_prime)}")

                # Check Normal Forms
                def check_normal_forms(relation_attrs, fds, keys):
                    all_attrs = set(relation_attrs)
                    prime = set("".join(keys))
                    key_sets = [set(k) for k in keys]

                    is_bcnf, is_3nf, is_2nf = True, True, True
                    for lhs, rhs in fds:
                        non_trivial_rhs = rhs - lhs
                        if not non_trivial_rhs:
                            continue
                        lhs_is_superkey = compute_closure(lhs, fds) == all_attrs
                        rhs_is_prime = non_trivial_rhs.issubset(prime)

                        if not lhs_is_superkey:
                            is_bcnf = False
                            if not rhs_is_prime:
                                is_3nf = False
                            # 2NF check: partial dependency
                            for k in key_sets:
                                if lhs.issubset(k) and lhs != k and not non_trivial_rhs.issubset(prime):
                                    is_2nf = False

                    return {"2NF": is_2nf, "3NF": is_3nf, "BCNF": is_bcnf}

                nf_status = check_normal_forms(R_attrs, F, keys)
                print("Normal Form Status:", nf_status)

                # Lossless Join Test for Decomposition R1(A, B, C), R2(C, D, E)
                R1, R2 = set("ABC"), set("CDE")
                common = R1.intersection(R2)
                closure_common = compute_closure(common, F)
                is_lossless = R1.issubset(closure_common) or R2.issubset(closure_common)
                print(f"Decomposition (ABC, CDE) Common: {common}, Closure: {closure_common}")
                print(f"Is Lossless Join? {is_lossless}")
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **NAT:** Consider a relation schema $R(A, B, C, D, E)$ with functional dependencies
                $F = \\{A \\to BC, CD \\to E, B \\to D, E \\to A\\}$. What is the total number
                of **candidate keys** for relation $R$?

                **MCQ:** Which of the following normal form decomposition guarantees is true?

                A. Decomposition into 3NF is always lossless and dependency preserving; decomposition into BCNF is always lossless but may not preserve dependencies.
                B. Decomposition into BCNF is always dependency preserving, but 3NF is not.
                C. Every relation in 3NF is also in BCNF.
                D. A relation with only two attributes can never be in BCNF.

                **MSQ:** Let relation $R(A, B, C, D)$ satisfy functional dependencies
                $F = \\{AB \\to C, C \\to D, D \\to A\\}$. Which of the following statements are TRUE?

                A. The candidate keys of $R$ are $AB, BC,$ and $BD$.
                B. Attribute $A$ is a prime attribute.
                C. The relation $R$ is in 3NF.
                D. The relation $R$ is in BCNF.
                """
            ),
            markdown(
                """
                ## Solutions

                NAT: **4**.
                The candidate keys are **$A, E, CD,$ and $BC$** (Total: 4).
                - $A^+ = \\{A, B, C, D, E\\} \\implies A$ is a CK.
                - $E \\to A \\implies E^+ = \\{A, B, C, D, E\\} \\implies E$ is a CK.
                - $(CD)^+ = \\{C, D, E, A, B\\} \\implies CD$ is a CK (minimal since $C^+ = \\{C\\}, D^+ = \\{D\\}$).
                - $(BC)^+$: $B \\to D \\implies BC \\to CD \\to E \\to A \\implies BC$ is a CK.

                MCQ: **A**. 3NF decomposition can always achieve both lossless join and dependency
                preservation simultaneously (via synthesis algorithm). BCNF decomposition guarantees
                lossless join, but some dependencies may be lost.

                MSQ: **A, B, C**.
                - Candidate keys:
                  - $(AB)^+ = \\{A, B, C, D\\} \\implies AB$ is a CK.
                  - $(BC)^+ = \\{B, C, D, A\\} \\implies BC$ is a CK.
                  - $(BD)^+ = \\{B, D, A, C\\} \\implies BD$ is a CK.
                  So A is true.
                - Prime attributes are all members of candidate keys: $\\{A, B, C, D\\}$. All attributes are prime!
                  Since all attributes are prime, every FD $X \\to Y$ has prime RHS, satisfying the 3NF condition.
                  So B and C are true.
                - D is false: In $C \\to D$, $C$ is not a superkey, violating BCNF.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/machine_learning/decision_trees_and_svm.ipynb",
        [
            markdown(
                """
                # Decision Trees, Support Vector Machines, and Neural Network Parameters

                **Syllabus mapping:** decision trees, support vector machine,
                bias-variance trade-off, multi-layer perceptron, feed-forward neural network.

                **Objectives:** compute Entropy, Information Gain, and Gini Impurity for
                decision tree splits; understand maximal margin hyperplanes and support vectors
                in SVM; calculate trainable parameter counts in multi-layer perceptrons.
                """
            ),
            markdown(
                """
                ## Theoretical Foundations

                ### 1. Decision Tree Splitting Metrics
                For dataset $S$ with class proportions $p_1, p_2, \\dots, p_C$:
                - **Entropy:** $H(S) = -\\sum_{i=1}^C p_i \\log_2(p_i)$
                - **Information Gain:** $IG(S, A) = H(S) - \\sum_{v \\in \\text{Values}(A)} \\frac{|S_v|}{|S|} H(S_v)$
                - **Gini Impurity:** $\\text{Gini}(S) = 1 - \\sum_{i=1}^C p_i^2$

                ### 2. Support Vector Machines (Linear Separable Case)
                The separating hyperplane is $\\mathbf{w}^T \\mathbf{x} + b = 0$.
                - Canonical form: $y_i (\\mathbf{w}^T \\mathbf{x}_i + b) \\ge 1$
                - **Margin Width:** $\\gamma = \\frac{2}{\\|\\mathbf{w}\\|}$
                - **Optimization Problem:** $\\min_{\\mathbf{w}, b} \\frac{1}{2} \\|\\mathbf{w}\\|^2$ subject to $y_i(\\mathbf{w}^T \\mathbf{x}_i + b) \\ge 1$.
                - Data points satisfying $y_i(\\mathbf{w}^T \\mathbf{x}_i + b) = 1$ are the **support vectors**.

                ### 3. Multi-Layer Perceptron (MLP) Parameter Counting
                For a fully connected feed-forward layer with $n_{in}$ inputs and $n_{out}$ neurons:
                - Weight matrix: $n_{in} \\times n_{out}$ parameters.
                - Bias vector: $n_{out}$ parameters.
                - Total parameters per layer: $n_{in} \\times n_{out} + n_{out} = (n_{in} + 1) \\times n_{out}$.
                """
            ),
            code(
                """
                import numpy as np

                # 1. Decision Tree Entropy & Information Gain
                def entropy(labels):
                    _, counts = np.unique(labels, return_counts=True)
                    probs = counts / len(labels)
                    return -np.sum(probs * np.log2(probs + 1e-12))

                def gini_impurity(labels):
                    _, counts = np.unique(labels, return_counts=True)
                    probs = counts / len(labels)
                    return 1.0 - np.sum(probs ** 2)

                # Sample data: 14 instances (9 Yes, 5 No)
                parent_labels = np.array([1]*9 + [0]*5)
                h_parent = entropy(parent_labels)
                gini_parent = gini_impurity(parent_labels)

                print(f"Parent Entropy: {h_parent:.4f}")
                print(f"Parent Gini:    {gini_parent:.4f}")

                # Feature A split: Left (6 Yes, 2 No), Right (3 Yes, 3 No)
                left_labels = np.array([1]*6 + [0]*2)
                right_labels = np.array([1]*3 + [0]*3)
                n_total = len(parent_labels)

                h_left = entropy(left_labels)
                h_right = entropy(right_labels)
                weighted_entropy = (len(left_labels)/n_total)*h_left + (len(right_labels)/n_total)*h_right
                info_gain = h_parent - weighted_entropy

                print(f"Weighted Child Entropy: {weighted_entropy:.4f}")
                print(f"Information Gain:       {info_gain:.4f}")

                # 2. Linear SVM Margin Computation
                # Hyperplane: 3*x1 + 4*x2 - 2 = 0 => w = [3, 4], b = -2
                w = np.array([3.0, 4.0])
                w_norm = np.linalg.norm(w)
                margin_width = 2.0 / w_norm
                print(f"\\nSVM weight norm ||w||: {w_norm:.2f}")
                print(f"SVM Margin Width 2/||w||: {margin_width:.4f}")

                # 3. Neural Network Parameter Counter
                def count_mlp_params(layer_sizes):
                    total = 0
                    for i in range(len(layer_sizes) - 1):
                        weights = layer_sizes[i] * layer_sizes[i+1]
                        biases = layer_sizes[i+1]
                        layer_total = weights + biases
                        print(f"Layer {i+1} ({layer_sizes[i]} -> {layer_sizes[i+1]}): {weights} weights + {biases} biases = {layer_total}")
                        total += layer_total
                    return total

                architecture = [10, 20, 15, 3]
                print(f"\\nMLP Architecture: {architecture}")
                total_params = count_mlp_params(architecture)
                print(f"Total Trainable Parameters: {total_params}")
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **NAT:** A fully connected Feedforward Neural Network has an input layer of
                10 neurons, a first hidden layer of 20 neurons, a second hidden layer of
                15 neurons, and an output layer of 3 neurons. Every neuron in the hidden
                and output layers includes a bias term. Calculate the **total number of
                trainable parameters** (weights plus biases) in this network.

                **MCQ:** In a binary classification problem using a linear Support Vector
                Machine, the optimal separating hyperplane is given by $3x_1 + 4x_2 - 5 = 0$,
                with canonical margin boundaries $3x_1 + 4x_2 - 5 = +1$ and $3x_1 + 4x_2 - 5 = -1$.
                What is the margin width of this classifier?

                A. 0.2
                B. 0.4
                C. 0.5
                D. 2.0

                **MSQ:** Which of the following statements regarding Decision Trees and SVMs are TRUE?

                A. In Decision Trees, the Gini impurity of a perfectly pure node is 0.
                B. Increasing the depth of a decision tree typically decreases its bias and increases its variance.
                C. In a linear SVM, removing a non-support vector training point does not alter the optimal decision boundary.
                D. Decision tree training is sensitive to monotonic transformations of individual features and requires feature scaling.
                """
            ),
            markdown(
                """
                ## Solutions

                NAT: **583**.
                - Layer 1 (Input to Hidden 1): $10 \\times 20$ weights $+ 20$ biases $= 200 + 20 = 220$.
                - Layer 2 (Hidden 1 to Hidden 2): $20 \\times 15$ weights $+ 15$ biases $= 300 + 15 = 315$.
                - Layer 3 (Hidden 2 to Output): $15 \\times 3$ weights $+ 3$ biases $= 45 + 3 = 48$.
                - Total trainable parameters: $220 + 315 + 48 = 583$.

                MCQ: **B**.
                The normal vector is $\\mathbf{w} = [3, 4]^T$.
                The Euclidean norm is $\\|\\mathbf{w}\\| = \\sqrt{3^2 + 4^2} = \\sqrt{25} = 5$.
                The margin width is:
                $$\\gamma = \\frac{2}{\\|\\mathbf{w}\\|} = \\frac{2}{5} = 0.4.$$

                MSQ: **A, B, C**.
                - A is true: $\\text{Gini} = 1 - 1^2 = 0$ for a pure node.
                - B is true: Deeper trees fit training data more closely (lower bias, higher risk of overfitting/variance).
                - C is true: The SVM boundary is determined exclusively by the support vectors on the margin.
                - D is false: Decision trees only use threshold order comparisons and are invariant to strictly monotonic feature scaling.
                """
            ),
        ],
    )

    write_notebook(
        "notebooks/ai/logic_and_alpha_beta.ipynb",
        [
            markdown(
                """
                # Propositional Logic, Resolution Refutation, and Alpha-Beta Pruning

                **Syllabus mapping:** search: adversarial; logic: propositional, predicate.

                **Objectives:** construct and evaluate truth tables; determine satisfiability,
                validity, and logical entailment; implement Minimax with Alpha-Beta pruning
                and trace pruned branch counts.
                """
            ),
            markdown(
                """
                ## Theoretical Foundations

                ### 1. Propositional Logic
                - **Validity (Tautology):** A sentence is valid if it is true in **all** models (e.g. $P \\lor \\neg P$).
                - **Satisfiability:** A sentence is satisfiable if it is true in **at least one** model.
                - **Entailment:** $\\alpha \\models \\beta$ iff in every model where $\\alpha$ is true, $\\beta$ is also true.
                - **Proof by Resolution Refutation:**
                  $$\\alpha \\models \\beta \\iff \\alpha \\land \\neg \\beta \\text{ is unsatisfiable (derives empty clause } \\Box).$$

                ### 2. Alpha-Beta Pruning in Adversarial Search
                Minimax explores all $O(b^d)$ game tree nodes. Alpha-Beta pruning maintains two bounds:
                - $\\alpha$: The best (highest) value found so far by any choice along the path for MAX. Initialized to $-\\infty$.
                - $\\beta$: The best (lowest) value found so far by any choice along the path for MIN. Initialized to $+\\infty$.

                **Pruning Condition:**
                Whenever $\\alpha \\ge \\beta$, the remaining children of the current node can be pruned because the opponent would never allow play to reach this state.
                - **Best-case complexity:** $O(b^{d/2})$, doubling the searchable search depth.
                """
            ),
            code(
                """
                from itertools import product

                # 1. Propositional Logic Truth Table Evaluator
                def evaluate_implication(p, q):
                    return (not p) or q

                def evaluate_biconditional(p, q):
                    return p == q

                # Test tautology: (P -> Q) or (Q -> P)
                models = list(product([True, False], repeat=2))
                is_tautology = True
                print("Model (P, Q) | (P -> Q) | (Q -> P) | (P -> Q) or (Q -> P)")
                print("-" * 55)
                for p, q in models:
                    p_imp_q = evaluate_implication(p, q)
                    q_imp_p = evaluate_implication(q, p)
                    result = p_imp_q or q_imp_p
                    if not result:
                        is_tautology = False
                    print(f"{str(p):<5} {str(q):<5} | {str(p_imp_q):<9} | {str(q_imp_p):<9} | {str(result)}")

                print(f"\\nFormula is a TAUTOLOGY: {is_tautology}")

                # 2. Minimax with Alpha-Beta Pruning Implementation
                def alphabeta_trace(node, depth, is_max, alpha, beta, path="Root"):
                    if isinstance(node, (int, float)):
                        print(f"  Leaf {path}: value = {node} [alpha={alpha}, beta={beta}]")
                        return node, 0

                    pruned_count = 0
                    if is_max:
                        val = -float('inf')
                        for i, child in enumerate(node):
                            child_path = f"{path}->C{i+1}"
                            child_val, p = alphabeta_trace(child, depth + 1, False, alpha, beta, child_path)
                            pruned_count += p
                            val = max(val, child_val)
                            alpha = max(alpha, val)
                            if beta <= alpha:
                                remaining = len(node) - (i + 1)
                                pruned_count += remaining
                                print(f"  ** PRUNED at {path}: beta ({beta}) <= alpha ({alpha}), skipped {remaining} branch(es) **")
                                break
                        return val, pruned_count
                    else:
                        val = float('inf')
                        for i, child in enumerate(node):
                            child_path = f"{path}->C{i+1}"
                            child_val, p = alphabeta_trace(child, depth + 1, True, alpha, beta, child_path)
                            pruned_count += p
                            val = min(val, child_val)
                            beta = min(beta, val)
                            if beta <= alpha:
                                remaining = len(node) - (i + 1)
                                pruned_count += remaining
                                print(f"  ** PRUNED at {path}: beta ({beta}) <= alpha ({alpha}), skipped {remaining} branch(es) **")
                                break
                        return val, pruned_count

                # Tree: Root (MAX) with two MIN children A: [3, 5], B: [2, 9]
                game_tree = [[3, 5], [2, 9]]
                print("\\n--- Tracing Alpha-Beta Pruning ---")
                root_val, pruned = alphabeta_trace(game_tree, 0, True, -float('inf'), float('inf'))
                print(f"\\nRoot Minimax Value: {root_val}")
                print(f"Total Pruned Subtrees/Leaves: {pruned}")
                """
            ),
            markdown(
                """
                ## GATE-Style Practice

                **NAT:** Consider a two-player zero-sum game tree with MAX at the root.
                The root has two MIN children, $A$ and $B$. Child $A$ has two leaf children
                with values $3$ and $5$ (evaluated from left to right). Child $B$ has two
                leaf children with values $2$ and $9$ (evaluated from left to right).
                Using Alpha-Beta pruning with standard left-to-right evaluation, how many
                leaf nodes are **pruned** (not evaluated)?

                **MCQ:** Which of the following propositional logic formulas is a **tautology**
                (valid in all models)?

                A. $(P \\to Q) \\to P$
                B. $(P \\to Q) \\lor (Q \\to P)$
                C. $(P \\land Q) \\to (P \\land \\neg Q)$
                D. $(P \\lor Q) \\to (P \\land Q)$

                **MSQ:** Which of the following statements regarding Alpha-Beta pruning are TRUE?

                A. Alpha-Beta pruning always returns the exact same minimax value at the root as standard Minimax search.
                B. In the best-case move ordering, Alpha-Beta pruning reduces the effective branching factor from $b$ to $\\sqrt{b}$.
                C. At a MAX node, the value of $\\alpha$ can only increase or remain unchanged.
                D. If $\\alpha \\ge \\beta$ at any node, searching further children of that node cannot alter the minimax decision of the parent.
                """
            ),
            markdown(
                """
                ## Solutions

                NAT: **1**.
                1. Child $A$ (MIN node):
                   - Left leaf: evaluates to 3. MIN bound becomes $\\min(\\infty, 3) = 3$.
                   - Right leaf: evaluates to 5. MIN bound becomes $\\min(3, 5) = 3$.
                   - Child $A$ returns value 3 to Root (MAX).
                2. Root (MAX node):
                   - Sets $\\alpha = \\max(-\\infty, 3) = 3$.
                3. Child $B$ (MIN node, with $\\alpha = 3, \\beta = \\infty$):
                   - Left leaf: evaluates to 2. MIN bound becomes $\\beta = \\min(\\infty, 2) = 2$.
                   - Pruning condition checked: $\\beta \\le \\alpha$ ($2 \\le 3$).
                   - **Cutoff triggered!** The right leaf (value 9) is pruned.
                Total leaves pruned: **1**.

                MCQ: **B**.
                - $(P \\to Q) \\lor (Q \\to P) \\equiv (\\neg P \\lor Q) \\lor (\\neg Q \\lor P) \\equiv (\\neg P \\lor P) \\lor (Q \\lor \\neg Q) \\equiv \\text{True} \\lor \\text{True} \\equiv \\text{True}$.
                This statement is unconditionally true in every boolean model.

                MSQ: **A, B, C, D**.
                All four statements are foundational theorems in adversarial search:
                - A: Pruning is sound and optimal; it discards only branches provably irrelevant to the root decision.
                - B: Best-case time complexity is $O(b^{d/2})$, which corresponds to branching factor $\\sqrt{b}$.
                - C: MAX only pushes the lower bound $\\alpha$ upward.
                - D: $\\alpha \\ge \\beta$ guarantees the ancestor already has a better or equal guaranteed alternative.
                """
            ),
        ],
    )


if __name__ == "__main__":
    build_all()

