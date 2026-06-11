# 📘 Machine Learning – Topic-Wise Guide

### 📚 Resources

Reference : https://github.com/khangich/machine-learning-interview/tree/master

* **Multicollinearity:**
  [Statistics by Jim](https://statisticsbyjim.com/regression/multicollinearity-in-regression-analysis/) | [YouTube](https://www.youtube.com/watch?v=Cba9LJ9lS8s)

* **Feature Scaling:**
  [Sebastian Raschka Blog](https://sebastianraschka.com/Articles/2014_about_feature_scaling.html)

* **Random Forest vs GBDT:**
  [Medium Comparison Article](https://medium.com/@aravanshad/gradient-boosting-versus-random-forest-cfa3fa8f0d80)

* **SMOTE (Synthetic Minority Over-sampling Technique):**
  [Original Paper – Arxiv](https://arxiv.org/pdf/1106.1813.pdf)

* **Discriminative vs Generative Models:**
  [Medium Article](https://medium.com/@mlengineer/generative-and-discriminative-models-af5637a66a3)
  [Stanford Paper by Ng & Jordan](http://ai.stanford.edu/~ang/papers/nips01-discriminativegenerative.pdf)

* **Logistic Regression:**
  [YouTube – Coding Explained](https://www.youtube.com/watch?v=-la3q9d7AKQ)
  *📝 Try implementing from scratch in NumPy – bonus for vectorized version and a MapReduce variant!*
  Sample Code: [`logistic_regression.ipynb`](https://github.com/khangich/machine-learning-interview/blob/master/sample/logistic_regression.ipynb)

* **Quantile Regression:**
  [YouTube Lecture](https://www.youtube.com/watch?v=s203ScTy4xQ&t=954s)

* **L1/L2 Regularization Intuition:**
  [LinkedIn Visual Intuition](https://www.linkedin.com/pulse/intuitive-visual-explanation-differences-between-l1-l2-xiaoli-chen/)

* **Decision Trees & Random Forests:**
  [MIT Slides](https://people.csail.mit.edu/dsontag/courses/ml16/slides/lecture11.pdf)

* **Boosting Fundamentals:**
  [Stanford Slides by Hastie](https://web.stanford.edu/~hastie/TALKS/boost.pdf)

* **Least Squares as MLE:**
  [YouTube Video](https://www.youtube.com/watch?v=_-Gnu498s3o)

* **MLE Introduction:**
  [YouTube Lecture](https://www.youtube.com/watch?v=WflqTUOvdik&t=15s)

* **K-Means Clustering:**
  [Stanford Notes](https://stanford.edu/~cpiech/cs221/handouts/kmeans.html)
  Sample Code: [`kmeans.ipynb`](https://github.com/khangich/machine-learning-interview/blob/master/sample/kmeans.ipynb)
  *📝 Implement from scratch – optimize initialization (e.g., k-means++).*

* **PCA Intuition:**
  [Neuronal Blog – PCA Explained](http://alexhwilliams.info/itsneuronalblog/2016/03/27/pca/)

* **Eigenvectors & Eigenvalues Visualization:**
  [Setosa.io](https://setosa.io/ev/eigenvectors-and-eigenvalues/)

* **SVD (Singular Value Decomposition):**
  [Gregory Gundersen Blog](https://gregorygundersen.com/blog/2018/12/10/svd/)

* **KL-Divergence:**
  [CountBayesie Blog](https://www.countbayesie.com/blog/2017/5/9/kullback-leibler-divergence-explained)

* **Cross Entropy:**
  [Colah’s Blog](https://colah.github.io/posts/2015-09-Visual-Information/)

* **Cheatsheet:**
  [ML Flashcards](https://machinelearningflashcards.com/) – optional but useful for quick revision.

---

## 🎓 Interview Experiences

### 🧑‍🏫 IIT MSR/AI Program Insights

* [IIT Bombay & Delhi (MS – MINDS & CMInDS) Experience](https://gateoverflow.in/blog/14429/iit-bombay-%26-delhi-ms-interview-experience-minds-%26-cminds)
* [IIT Indore MSR Experience (Reddit)](https://www.reddit.com/r/GATEtard/comments/1kfakyn/iit_indore_msr_interview_experience/)
* [IIT Delhi MSR AI Interview Blog](https://gateoverflow.in/blog/15907/iit-delhi-masters-research-ai-experience)

# Extra reads	
## ML advance topics
| Paper | Why |
| ------------- | ------------- |
| [Sampling techniques](https://www.ml-science.com/sampling) | Stratifield sampling is popular. |
| [A Comparative Study of Efficient Initialization Methods for the k-means Clustering Algorithm](https://arxiv.org/pdf/1209.1960.pdf) and [kmeans initialization, Coursera](https://www.coursera.org/lecture/cluster-analysis/3-3-initialization-of-k-means-clustering-bPyBl)| Fundamentals about kemans, favourite topics in interviews i.e: LinkedIn|
| [A Comprehensive Survey of Clustering Algorithms](https://link.springer.com/content/pdf/10.1007/s40745-015-0040-1.pdf) | Clustering fundamentals |
| [A Tutorial on Spectral Clustering](https://arxiv.org/pdf/0711.0189.pdf)| Sepctral clustering is intuitive and quite popular. |
| [Partial residual plot](https://en.wikipedia.org/wiki/Partial_residual_plot) | Useful for model diagnosis. |
| [Compare GINI index and Information Gain](https://www.unine.ch/files/live/sites/imi/files/shared/documents/papers/Gini_index_fulltext.pdf) | Intuition behind Decision Tree, RandomForest |
| [Explain tf-idf](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.97.7340&rep=rep1&type=pdf) | Fundamentals about tf-idf. |
| [Understanding L-BFGS](https://aria42.com/blog/2014/12/understanding-lbfgs) | Advance about optimization, rarely asked in interview |
| [Optimizer Quasi newton method](http://www.seas.ucla.edu/~vandenbe/236C/lectures/qnewton.pdf) | Advance about optimization. |


## DL classic papers
| Paper | Why |
| ------------- | ------------- |
| [Understanding the Difficulty of Training Deep Feedforward Neural Networks](http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf) | Classic paper (2010) about initialization, sigmoid etc |
| [Delving Deep into Rectifiers - Surpassing Human-Level Performance on ImageNet Classification](https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/He_Delving_Deep_into_ICCV_2015_paper.pdf) | Classic paper (2015) about ReLU, PReLU|
| [Batch Normalization - Accelerating Deep Network Training by Reducing Internal Covariate Shift](https://arxiv.org/abs/1502.03167) | Classic paper about BatchNorm |
| [Dropout - A Simple Way to Prevent Neural Networks from Overfitting](https://www.jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf) | Classic paper about Dropout |
| [Deep Residual Learning for Image Recognition](https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf) | Classic ResNet |
| [On Large-Batch Training for Deep Learning - Generalization Gap and Sharp Minima](https://arxiv.org/abs/1609.04836) | Practical technique for large batch training |


## DL advance topics
| Paper | Why |
| ------------- | ------------- |
| [Calibration in modern neural network](https://arxiv.org/pdf/1706.04599.pdf) | Important topics in ML system design i.e: facebook |
| [Attention model](https://www.youtube.com/watch?v=quoGRI-1l0A&list=RDCMUCcIXc5mJsHVYTZR1maL5l9w&index=2) | Fundamentals in Attention, powerful architecture in NLP |
| [Ilya's thesis](https://www.cs.utoronto.ca/~ilya/pubs/ilya_sutskever_phd_thesis.pdf) | Network in network |


## NLP
| Paper | Why |
| ------------- | ------------- |
| [Adaptive Importance Sampling to Accelerate Training of a Neural Probabilistic Language Model](https://wiki.inf.ed.ac.uk/twiki/pub/CSTR/ListenSemester2_2009_10/4443871.pdf) | Classic paper (2008) in NLP |
| [Natural Language Processing (Almost) from Scratch](https://www.jmlr.org/papers/volume12/collobert11a/collobert11a.pdf) | Classic paper (2011) in NLP |
| [Word2vec](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf) | The classic paper in NLP, still popular in industry: Uber, DoorDash, Twitter etc |
| [GloVe - Global Vectors for Word Representation](https://www.aclweb.org/anthology/D14-1162.pdf) | Classic paper (2014) in NLP |
| [Bag of Tricks for Efficient Text Classification](https://arxiv.org/pdf/1607.01759.pdf) | Cool tricks in NLP tasks |
| [BERT - Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/pdf/1810.04805.pdf) | The famous BERT |
| [Smart Reply - Automated Response Suggestion for Email](https://arxiv.org/pdf/1606.04870.pdf) | NLP application, useful for ML system design |
| [Enriching Word Vectors with Subword Information](https://www.mitpressjournals.org/doi/pdfplus/10.1162/tacl_a_00051) | Simple and fast method to train NLP task in Facebook|
| [Neural Approaches to Conversational AI](https://arxiv.org/pdf/1809.08267.pdf) | Comprehensive survey (2018) about chatbots|

## Recent breakthrough
- [Feb 2021, recent breakthrough ClubHouse chat](https://victordibia.com/blog/ai-breakthroughs-feb21/)

---
