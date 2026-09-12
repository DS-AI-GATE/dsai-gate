# GATE DA Past Years Question Analysis & 2027 Syllabus Mapping

This document provides a systematic syllabus mapping and analysis of all 195 questions from official GATE Data Science and Artificial Intelligence (DA) papers: **GATE DA 2024** (IISc Bangalore), **GATE DA 2025** (IIT Roorkee), and **GATE DA 2026** (IIT Guwahati), cross-referenced with the **official GATE DA 2027 syllabus** (IIT Madras).

---

## 1. Exam Pattern & Marks Breakdown

The GATE DA paper consists of **65 questions** totaling **100 marks** with a 3-hour duration:
- **General Aptitude (GA)**: Questions 1 to 10 (15 Marks)
  - Q.1 – Q.5: 1 mark each (5 marks)
  - Q.6 – Q.10: 2 marks each (10 marks)
- **Data Science and AI (DA)**: Questions 11 to 65 (85 Marks)
  - Q.11 – Q.35: 1 mark each (25 marks)
  - Q.36 – Q.65: 2 marks each (60 marks)

### Question Types & Marking Schemes
1. **Multiple Choice Questions (MCQ)**: Only 1 option correct. Negative marking: $-\frac{1}{3}$ for 1-mark questions, $-\frac{2}{3}$ for 2-mark questions.
2. **Multiple Select Questions (MSQ)**: 1 or more options correct. Full marks only if all correct choices and no wrong choices are selected. **No negative marking, no partial marking**.
3. **Numerical Answer Type (NAT)**: Real number entered via virtual numeric keypad. **No negative marking**.

---

## 2. Subject-Wise Weightage Trends (2024 – 2026)

| Section | 2024 Weightage | 2025 Weightage | 2026 Weightage | Average Weightage | Priority Level for 2027 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **General Aptitude (GA)** | 15 Marks | 15 Marks | 15 Marks | **15 Marks (15%)** | High (High scoring) |
| **Probability & Statistics** | 16 Marks | 15 Marks | 17 Marks | **16 Marks (16%)** | Highest (Foundational) |
| **Linear Algebra** | 12 Marks | 13 Marks | 11 Marks | **12 Marks (12%)** | High |
| **Calculus & Optimization** | 5 Marks | 6 Marks | 5 Marks | **5.3 Marks (5.3%)** | Medium (Single Variable) |
| **Programming, DSA** | 11 Marks | 12 Marks | 11 Marks | **11.3 Marks (11.3%)** | High |
| **DBMS & Data Warehousing** | 13 Marks | 12 Marks | 13 Marks | **12.7 Marks (12.7%)** | High |
| **Machine Learning** | 16 Marks | 15 Marks | 16 Marks | **15.7 Marks (15.7%)** | Highest |
| **Artificial Intelligence** | 12 Marks | 12 Marks | 12 Marks | **12 Marks (12%)** | High |
| **Total** | **100 Marks** | **100 Marks** | **100 Marks** | **100 Marks** | |

---

## 3. High-Yield Topic Analysis by Subject

### Section 1: Probability and Statistics (15–17 Marks)
- **Top Recurring Topics**:
  1. *Bayes' Theorem & Conditional Probability*: Sensitivity, specificity, disease testing, posterior probabilities.
  2. *Statistical Inference & Hypothesis Testing*: $z$-tests, two-sample $t$-tests, confidence intervals, rejection regions, p-values.
  3. *Distributions*: Binomial PMF, Poisson rates, Normal distribution standardization ($Z = \frac{X-\mu}{\sigma}$), Exponential memoryless property.
  4. *Joint Distributions & Conditional Expectation*: Marginal densities, covariance, correlation coefficient $\rho(X, Y) = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y}$.
- **Key Pitfall**: Confusing discrete vs continuous distributions; forgetting that the sample standard deviation in $t$-tests uses divisor $n-1$ (Bessel's correction).

### Section 2: Linear Algebra (11–13 Marks)
- **Top Recurring Topics**:
  1. *Eigenvalues & Eigenvectors*: Characteristic polynomials, trace = sum of eigenvalues, determinant = product of eigenvalues.
  2. *Rank-Nullity Theorem & Linear Systems*: Dimension theorem ($\text{rank}(A) + \text{nullity}(A) = n$), consistency criterion ($\text{rank}(A) = \text{rank}([A|b])$).
  3. *Projections & Orthogonality*: Projection matrix $P = A(A^TA)^{-1}A^T$, idempotent property $P^2 = P$, orthogonal complements.
  4. *Singular Value Decomposition (SVD)*: Singular values as square roots of non-zero eigenvalues of $A^TA$, rank-k matrix approximation.
  5. *Partition Matrices*: Determinants and inverses of block triangular matrices $\det \begin{bmatrix} A & B \\ 0 & D \end{bmatrix} = \det(A)\det(D)$.

### Section 3: Calculus and Optimization (5–6 Marks)
- **Top Recurring Topics**:
  1. *Single-Variable Optimization*: First and second derivative tests, global extrema on closed intervals $[a, b]$.
  2. *Taylor Series Expansions*: Maclaurin series for $e^x, \sin x, \cos x, \ln(1+x)$, truncation error bounds.
  3. *Limits & Continuity*: Indeterminate forms, L'Hôpital's rule, piecewise continuous functions.
- **Syllabus Boundary**: Scope is strictly *single-variable*. Multivariable gradients, Hessians, and multivariable Lagrange multipliers are outside this section.

### Section 4: Programming, Data Structures and Algorithms (11–12 Marks)
- **Top Recurring Topics**:
  1. *Python Code Tracing*: Scope resolution (LEGB rule), mutable default arguments in functions, recursion tree tracing, list comprehensions.
  2. *Asymptotic Analysis & Recurrences*: Master theorem cases, loop comparison counters, logarithmic search complexity.
  3. *Sorting & Searching*: Binary search on sorted arrays, partition step of quicksort, mergesort comparison bounds.
  4. *Trees & Binary Search Trees*: Tree traversals (in-order BST produces sorted output), height/node relationships.
  5. *Graph Algorithms*: BFS (queue-based, shortest path in unweighted graphs), DFS (cycle detection), Dijkstra's algorithm.

### Section 5: Database Management and Warehousing (12–13 Marks)
- **Top Recurring Topics**:
  1. *Relational Algebra & SQL*: Group By / Having clauses, subqueries, natural joins, outer joins, division operator.
  2. *Normalization*: Functional dependency closures, finding candidate keys, 3NF vs BCNF testing, dependency preservation.
  3. *Tuple Relational Calculus (TRC)*: Translating declarative relational calculus expressions with quantifiers ($\forall, \exists$) into relational algebra.
  4. *Indexing & B+ Trees*: Order of B+ tree, maximum and minimum keys per leaf and internal node, block access calculations.
  5. *Data Warehousing*: Star vs Snowflake schemas, concept hierarchies, classification of measures (additive, semi-additive, non-additive).

### Section 6: Machine Learning (15–17 Marks)
- **Top Recurring Topics**:
  1. *Supervised Linear Models*: Linear regression normal equation, Ridge regularized analytical solution $(\mathbf{X}^T\mathbf{X} + \lambda \mathbf{I})^{-1}\mathbf{X}^T\mathbf{y}$, Logistic regression sigmoid boundary.
  2. *Decision Trees*: Entropy calculation, Information Gain, Gini Impurity, pruning behavior.
  3. *Support Vector Machines*: Maximal margin $\frac{2}{\|\mathbf{w}\|}$, support vector identification, soft-margin slack variables.
  4. *Clustering*: k-means clustering iteration steps, convergence to local minimum, single-linkage vs complete-linkage dendrogram construction.
  5. *PCA & Dimensionality Reduction*: Covariance matrix projection, variance explained ratio $\frac{\lambda_1}{\sum \lambda_i}$.
  6. *Multi-Layer Perceptron*: Layer dimension matrix multiplications, total parameter calculations, activation function properties.

### Section 7: Artificial Intelligence (11–13 Marks)
- **Top Recurring Topics**:
  1. *Informed & Uninformed Search*: A* search admissibility ($h(n) \le h^*(n)$) and consistency, BFS/DFS time and space complexity.
  2. *Adversarial Search*: Minimax value computation, Alpha-Beta pruning condition ($\alpha \ge \beta$), branch cutoff counts.
  3. *Propositional & Predicate Logic*: Truth table satisfiability, tautology verification, CNF conversion, resolution refutation proofs.
  4. *Reasoning Under Uncertainty*: Bayesian network conditional independence (d-separation), exact inference via variable elimination, sampling methods.

---

## 4. Master Question-to-Syllabus Mapping Matrix

### 4.1 Sample Representative Mappings (GATE DA 2024)

| Q. No | Type | Marks | Official Key | Syllabus Section | Sub-Topic | Core Mathematical Concept |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Q.1–Q.10** | MCQ | 1 & 2 | Official Key | General Aptitude | Verbal, Quantitative, Spatial | Reading comprehension, geometry, series, spatial rotation |
| **Q.11** | MCQ | 1 | Official Key | Probability & Stats | Random Variables & Expectations | Linearity of expectation $E[aX + b] = aE[X] + b$ |
| **Q.12** | MCQ | 1 | Official Key | Linear Algebra | Matrices & Determinants | Determinant properties and rank of product $AB$ |
| **Q.13** | MCQ | 1 | Official Key | Calculus & Opt | Functions of single variable | Limit computation and L'Hôpital's rule |
| **Q.14** | MCQ | 1 | Official Key | Programming & DSA | Python Semantics | List slicing and mutable reference updates |
| **Q.15** | MCQ | 1 | Official Key | DBMS | Relational Algebra | Equivalence of cross-product followed by selection to join |
| **Q.16** | MCQ | 1 | Official Key | Machine Learning | Supervised Learning | Decision boundary linearity of Logistic Regression |
| **Q.17** | MCQ | 1 | Official Key | AI | Search Algorithms | A* admissibility condition guaranteeing optimal solution |
| **Q.18** | MCQ | 1 | Official Key | Probability & Stats | Distributions | Poisson PMF calculation $P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!}$ |
| **Q.19** | MCQ | 1 | Official Key | Linear Algebra | Eigenvalues & Eigenvectors | Trace and determinant relations for eigenvalues |
| **Q.20** | MCQ | 1 | Official Key | Programming & DSA | Asymptotic Complexity | Big-O bounds for divide-and-conquer recurrences |
| **Q.30** | NAT | 1 | `0 to 0` | Linear Algebra | Vector Spaces & Projections | Projection of orthogonal vector onto subspace |
| **Q.31** | NAT | 1 | `3 to 3` | DBMS | Normal Forms | Candidate key count for given functional dependencies |
| **Q.32** | NAT | 1 | `17 to 17` | Programming & DSA | Sorting & Searching | Number of comparisons in binary search |
| **Q.33** | NAT | 1 | `0.24 to 0.24` | Probability & Stats | Bayes' Theorem | Conditional probability calculation |
| **Q.34** | NAT | 1 | `42 to 42` | Machine Learning | Neural Networks | Trainable parameter count in multi-layer perceptron |
| **Q.35** | NAT | 1 | `0 to 0` | AI | Adversarial Search | Number of leaves pruned in Alpha-Beta search |
| **Q.36–Q.65** | MCQ/MSQ/NAT | 2 | Official Key | DA Core (All 7 Sections) | Advanced Problem Solving | Multi-step derivations, BCNF decomposition, SVM margins, SVD |

---

## 5. Recommended Study Progression for GATE DA 2027

```
Phase 1: Mathematical Foundations (Months 1–2)
├── Linear Algebra (Vector spaces, Eigenvalues, SVD, Block matrices)
├── Calculus (Single-variable limits, Taylor series, Optimization)
└── Probability & Statistics (Axioms, Distributions, CLT, Hypothesis tests)
       │
       ▼
Phase 2: Core Computer Science & Systems (Months 3–4)
├── Programming in Python (Scoping, Generators, Comprehensions)
├── Data Structures & Algorithms (Trees, Graphs, Sorting, Divide & Conquer)
└── DBMS & Warehousing (SQL, Relational Algebra, TRC, BCNF, B+ Trees)
       │
       ▼
Phase 3: Machine Learning & Artificial Intelligence (Months 5–6)
├── Machine Learning (Regression, Classifiers, SVM, Trees, Clustering, MLP)
└── Artificial Intelligence (A* search, Alpha-Beta, Logic, Bayesian Networks)
       │
       ▼
Phase 4: PYQ Rigor, Revision & Mock Tests (Months 7–8)
├── Solve all 65 questions of GATE DA 2024, 2025, and 2026 under timed conditions
├── Target high accuracy in General Aptitude (15/15 target)
└── Focus on MSQ and NAT error elimination using repo notebooks
```
