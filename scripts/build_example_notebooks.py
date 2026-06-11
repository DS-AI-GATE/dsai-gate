"""Build the repository's small, deterministic example notebooks."""

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]


def markdown(text):
    return nbf.v4.new_markdown_cell(dedent(text).strip())


def code(text):
    return nbf.v4.new_code_cell(dedent(text).strip())


def write_notebook(relative_path, cells):
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
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, path)


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
