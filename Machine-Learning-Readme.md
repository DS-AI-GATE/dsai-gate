# Machine-Learning

[Table of Contents](#table-of-contents)  
* [Books](#books)  
* [NPTEL and MOOCs Courses](#course)  
* [Notes](#notes)  
* [Articles](#articles)  
* [Practice Problems](#practice-problems)



[<img src="/Data/Machine-Learning/Machine_Learning_Cheatsheet.png">](/Data/Machine-Learning/super-cheatsheet-machine-learning.pdf)
> [Download Full Pdf](/Data/Artificial-Intelligence/All_cheat_sheet.pdf)
 
Credits : [Stanford Cheatsheets: Machine Learning, AI, Probability Statistics, Deep Learning](https://stanford.edu/~shervine/teaching/) - Afshine Amidi and Shervine Amidi published on September 8, 2019

<!-- subject-diagram:start -->
## Interactive Concept Map

Open the Mermaid diagram viewer on GitHub to pan and zoom through this original
subject map.

```mermaid
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
    classDef default fill:#172033,stroke:#58c4dd,color:#ffffff,stroke-width:2px
    linkStyle default stroke:#f2cc8f,stroke-width:2px
```

Diagram style follows a visual-first progression inspired by [3Blue1Brown](https://www.3blue1brown.com/).
<!-- subject-diagram:end -->

---

## <a name="books"></a>Books

Explore these recommended books to enhance your understanding:

<!--
- [**"All of Statistics: A Concise Course in Statistical Inference"**](https://egrcc.github.io/docs/math/all-of-statistics.pdf) by  Larry Wasserman 
  A comprehensive resource for statistical theory and its applications.
-->

- [**Probabilistic Machine Learning: An Introduction**](https://probml.github.io/pml-book/book1.html) by Kevin P. Murphy\
  The author's official page includes the licensed draft, exercises, and code.

 - [**Learning from Data**](https://openeclass.panteion.gr/modules/document/file.php/PMS152/LEARNING/Abu-Mostafa%20Yaser%20S.%2C%20Malik%20Magdon-Ismail%2C%20Hsuan-Tien%20Lin%20%282012%29%20--%20Learning%20From%20Data_%20A%20short%20course.pdf) course book for IIT D undergraduate level ML course

- [**Machine Learning Book**](http://www.cs.cmu.edu/~tom/mlbook.html) by  Tom M. Mitchell (CMU)\
  A classical book for Machine Learning.
---

## <a name="course"></a>NPTEL and MOOCs Courses

Course to deepen your knowledge:

- [**"Introduction to Machine Learning IIT Delhi"**](https://www.cse.iitd.ac.in/~parags/teaching/col774/) by  Prof [Parag Singla((IIT-D)](https://www.cse.iitd.ac.in/~parags/)
  A comprehensive resource for ML theory, excellent coverage from GATE and Interviews perspective.

- [**"Stanford CS229: Machine Learning Full Course taught by Andrew Ng"**](https://www.youtube.com/watch?v=jGwO_UgTS7I&list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU&ab_channel=StanfordOnline) by  Prof Andrew NG (Stanford) \
This course provides a broad introduction to machine learning and statistical pattern recognition. Topics include: supervised learning (generative/discriminative learning, parametric/non-parametric learning, neural networks, support vector machines); unsupervised learning (clustering, dimensionality reduction, kernel methods); learning theory (bias/variance tradeoffs, practical advice);

- [**Learning from Data: Caltech course Lectures**](https://home.work.caltech.edu/telecourse.html) \
This is an introductory course in machine learning (ML) that covers the basic theory, algorithms, and applications. ML is a key technology in Big Data, and in many financial, medical, commercial, and scientific applications. || **[NTU MOOC : Learning from Data](https://www.csie.ntu.edu.tw/~htlin/mooc/)**

---


## <a name="notes"></a>Notes

Review these comprehensive notes to reinforce your grasp:

- **[Stanford CS229 Lecture Notes](https://cs229.stanford.edu/main_notes.pdf)** sufficient to cover entire syllabus of Machine Learning \
Repository contains the pdf notes :[download_here](/Data/Machine-Learning/main_notes.pdf)
- **[CMU Machine Learning Notes](https://www.cs.cmu.edu/~hn1/documents/machine-learning/notes.pdf)** by Huy NguyenPhD Student, Human-Computer Interaction Institute, Carnegie Mellon University \

---

## <a name="articles"></a>Articles

Read insightful articles to gain additional insights:

**Coding Examples** : [**Kevin Murphy : A Probabilistic Perspective Book Coding Examples**](https://github.com/probml/pyprobml/tree/master)\
Python 3 code to reproduce the figures in the books [Probabilistic Machine Learning: An Introduction](https://probml.github.io/pml-book/book1.html) (aka "book 1") and [Probabilistic Machine Learning: Advanced Topics](https://probml.github.io/pml-book/book2.html) (aka "book 2"). The code uses the standard Python libraries, such as numpy, scipy, matplotlib, sklearn, etc.

**Repository Examples**

- [Linear regression from scratch](notebooks/machine_learning/linear_regression_from_scratch.ipynb)
- [Logistic classification](notebooks/machine_learning/logistic_classification.ipynb)
- [K-means from scratch](notebooks/machine_learning/kmeans_from_scratch.ipynb)

The example sequence is informed by collaborator
[Swakath's PRML assignment repository](https://github.com/swakath/PRML), with
original GATE-focused explanations, code, and data.

---

## <a name="practice-problems"></a>Practice Problems

Test your knowledge and skills with these practice problems:

- **[Berkley CS 189 Machine Learning Previous Year Questions and Solutions](https://tbp.berkeley.edu/courses/cs/189/)**
- **[Learning from Data Homework Caltech: MCQ Questions and Solutions](https://home.work.caltech.edu/homeworks.html)**


- [UNIVERSITY of PENNSYLVANIA CIS 520: Machine Learning; MCQ 2017 Final](/Data/Machine-Learning/final2017_solutions.pdf)
- [UNIVERSITY of PENNSYLVANIA CIS 520: Machine Learning; MCQ 2018 Final](/Data/Machine-Learning/final2018_solutions.pdf)
- [UNIVERSITY of PENNSYLVANIA CIS 520: Machine Learning; MCQ 2019 Final](/Data/Machine-Learning/final2019_solutions.pdf)
- [UNIVERSITY of PENNSYLVANIA CIS 520: Machine Learning; MCQ 2022 Final](/Data/Machine-Learning/final2022.pdf)
- [UNIVERSITY of PENNSYLVANIA CIS 520: Machine Learning; MCQ 2018 MidTerm](/Data/Machine-Learning/midterm2018_solutions.pdf)
- [UNIVERSITY of PENNSYLVANIA CIS 520: Machine Learning; MCQ 2019 MidTerm](/Data/Machine-Learning/midterm2019_solutions.pdf)
- [UNIVERSITY of PENNSYLVANIA CIS 520: Machine Learning; MCQ 2022 MidTerm](/Data/Machine-Learning/midterm2022_solutions.pdf)
- [Regression problems from IIT Dharwad EE 405: Patter Recognition and Machine Learning](/Data/Machine-Learning/python-practice-problems/regression)

---

[<img src="https://github.com/trekhleb/homemade-machine-learning/blob/master/images/machine-learning-map.png">](https://github.com/trekhleb/homemade-machine-learning/blob/master/images/machine-learning-map.png)
Machine Learning Mind Map


---

**Youtube courses** 📺 🖥️ :

- [**Advanced Introduction to Machine Learning | Winter 2023**](https://www.youtube.com/watch?v=nB77M-mm0Nk&list=PLLB0NZP0teC-JfhvTuaurDq6hSEzSy1cG&ab_channel=ByteSizeML) \
Course Syllabus : Motivation and Linear Regression, Binary Classification, Multi-class Classification, Clustering, Anomaly Detection, Data Visualization, Deep Learning Motivation. Deep Learning Mechanics,Deep Learning in NLP, Advanced Topics || **[Course Website](https://bytesizeml.github.io/ml2023/)**

#### <a name="table-of-contents"></a>Table of Contents

* [Books](#books)  
* [NPTEL and MOOCs Courses](#course)  
* [Notes](#notes)  
* [Articles](#articles)  
* [Practice Problems](#practice-problems)
