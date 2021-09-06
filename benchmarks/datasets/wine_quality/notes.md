# Wine Quality Dataset

**Source**: https://archive.ics.uci.edu/ml/datasets/wine+quality

# MindsDB note:
For a bigger challenge, we have merged both red and white information under one CSV file.

# Description:
Two datasets are included, related to red and white "vinho verde" wine samples, from the north of Portugal.
The goal is to model wine quality based on physicochemical tests.

Due to privacy and logistic issues, only physicochemical (inputs) and sensory (the output) variables are available
(e.g. there is no data about grape types, wine brand, wine selling price, etc.).

These datasets can be viewed as classification or regression tasks.
The classes are ordered and not balanced (e.g. there are many more normal wines than excellent or poor ones).
Outlier detection algorithms could be used to detect the few excellent or poor wines.
Also, we are not sure if all input variables are relevant.
So it could be interesting to test feature selection methods.

# Input variables (based on physicochemical tests):
1) Fixed acidity
2) Volatile acidity
3) Citric acid
4) Residual sugar
5) Chlorides
6) Free sulfur dioxide
7) Total sulfur dioxide
8) Density
9) pH
10) Sulphates
11) Alcohol


Output variable:
1) Sensed quality (score between 0 and 10)
